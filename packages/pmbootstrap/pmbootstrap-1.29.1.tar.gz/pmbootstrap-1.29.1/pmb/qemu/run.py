# Copyright 2021 Pablo Castellano, Oliver Smith
# SPDX-License-Identifier: GPL-3.0-or-later
import logging
import os
import re
import signal
import shlex
import shutil

import pmb.build
import pmb.chroot
import pmb.chroot.apk
import pmb.chroot.other
import pmb.chroot.initfs
import pmb.config
import pmb.helpers.run
import pmb.parse.arch
import pmb.parse.cpuinfo


def system_image(args):
    """
    Returns path to rootfs for specified device. In case that it doesn't
    exist, raise and exception explaining how to generate it.
    """
    path = args.work + "/chroot_native/home/pmos/rootfs/" + args.device + ".img"
    if not os.path.exists(path):
        logging.debug("Could not find rootfs: " + path)
        raise RuntimeError("The rootfs has not been generated yet, please "
                           "run 'pmbootstrap install' first.")
    return path


def create_second_storage(args):
    """
    Generate a second storage image if it does not exist.
    :returns: path to the image or None
    """
    path = f"{args.work}/chroot_native/home/pmos/rootfs/{args.device}-2nd.img"
    pmb.helpers.run.root(args, ["touch", path])
    pmb.helpers.run.root(args, ["chmod", "a+w", path])
    resize_image(args, args.second_storage, path)
    return path


def which_qemu(args, arch):
    """
    Finds the qemu executable or raises an exception otherwise
    """
    executable = "qemu-system-" + arch
    if shutil.which(executable):
        return executable
    else:
        raise RuntimeError("Could not find the '" + executable + "' executable"
                           " in your PATH. Please install it in order to"
                           " run qemu.")


def create_gdk_loader_cache(args):
    """
    Create a gdk loader cache that can be used for running GTK UIs outside of
    the chroot.
    """
    gdk_cache_dir = "/usr/lib/gdk-pixbuf-2.0/2.10.0/"
    custom_cache_path = gdk_cache_dir + "loaders-pmos-chroot.cache"
    rootfs_native = args.work + "/chroot_native"
    if os.path.isfile(rootfs_native + custom_cache_path):
        return rootfs_native + custom_cache_path

    cache_path = gdk_cache_dir + "loaders.cache"
    if not os.path.isfile(rootfs_native + cache_path):
        raise RuntimeError("gdk pixbuf cache file not found: " + cache_path)

    pmb.chroot.root(args, ["cp", cache_path, custom_cache_path])
    cmd = ["sed", "-i", "-e",
           "s@\"" + gdk_cache_dir + "@\"" + rootfs_native + gdk_cache_dir + "@",
           custom_cache_path]
    pmb.chroot.root(args, cmd)
    return rootfs_native + custom_cache_path


def command_qemu(args, arch, img_path, img_path_2nd=None):
    """
    Generate the full qemu command with arguments to run postmarketOS
    """
    cmdline = args.deviceinfo["kernel_cmdline"]
    if args.cmdline:
        cmdline = args.cmdline

    if "video=" not in cmdline:
        cmdline += " video=" + args.qemu_video

    logging.debug("Kernel cmdline: " + cmdline)

    port_ssh = str(args.port)

    suffix = "rootfs_" + args.device
    rootfs = args.work + "/chroot_" + suffix
    flavor = pmb.chroot.other.kernel_flavors_installed(args, suffix)[0]
    ncpus = os.cpu_count()

    if args.host_qemu:
        qemu_bin = which_qemu(args, arch)
        env = {}
        command = [qemu_bin]
    else:
        rootfs_native = args.work + "/chroot_native"
        env = {"QEMU_MODULE_DIR": rootfs_native + "/usr/lib/qemu",
               "GBM_DRIVERS_PATH": rootfs_native + "/usr/lib/xorg/modules/dri",
               "LIBGL_DRIVERS_PATH": rootfs_native + "/usr/lib/xorg/modules/dri"}

        if "gtk" in args.qemu_display:
            gdk_cache = create_gdk_loader_cache(args)
            env.update({"GTK_THEME": "Default",
                        "GDK_PIXBUF_MODULE_FILE": gdk_cache,
                        "XDG_DATA_DIRS": rootfs_native + "/usr/local/share:" +
                        rootfs_native + "/usr/share"})

        command = []
        if args.arch_native in ["aarch64", "armv7"]:
            # Workaround for QEMU failing on aarch64 asymetric multiprocessor arch
            # (big/little architecture https://en.wikipedia.org/wiki/ARM_big.LITTLE)
            # see https://bugs.linaro.org/show_bug.cgi?id=1443
            ncpus_bl = pmb.parse.cpuinfo.arm_big_little_first_group_ncpus()
            if ncpus_bl:
                ncpus = ncpus_bl
                logging.info("QEMU will run on big/little architecture on the"
                             f" first {ncpus} cores (from /proc/cpuinfo)")
                command += [rootfs_native + "/lib/ld-musl-" +
                            args.arch_native + ".so.1"]
                command += [rootfs_native + "/usr/bin/taskset"]
                command += ["-c", "0-" + str(ncpus - 1)]

        command += [rootfs_native + "/lib/ld-musl-" +
                    args.arch_native + ".so.1"]
        command += ["--library-path=" + rootfs_native + "/lib:" +
                    rootfs_native + "/usr/lib:" +
                    rootfs_native + "/usr/lib/pulseaudio"]
        command += [rootfs_native + "/usr/bin/qemu-system-" + arch]
        command += ["-L", rootfs_native + "/usr/share/qemu/"]

    command += ["-nodefaults"]
    command += ["-kernel", rootfs + "/boot/vmlinuz-" + flavor]
    command += ["-initrd", rootfs + "/boot/initramfs-" + flavor]
    command += ["-append", shlex.quote(cmdline)]

    command += ["-smp", str(ncpus)]

    command += ["-m", str(args.memory)]

    command += ["-serial", "stdio"]

    command += ["-drive", "file=" + img_path + ",format=raw,if=virtio"]
    if img_path_2nd:
        command += ["-drive", "file=" + img_path_2nd + ",format=raw,if=virtio"]

    if args.qemu_tablet:
        command += ["-device", "virtio-tablet-pci"]
    else:
        command += ["-device", "virtio-mouse-pci"]
    command += ["-device", "virtio-keyboard-pci"]
    command += ["-nic",
                "user,model=virtio-net-pci,"
                "hostfwd=tcp::" + port_ssh + "-:22,"
                ]

    if arch == "x86_64":
        command += ["-vga", "virtio"]
    elif arch == "aarch64":
        command += ["-M", "virt"]
        command += ["-cpu", "cortex-a57"]
        command += ["-device", "virtio-gpu-pci"]
    else:
        raise RuntimeError("Architecture {} not supported by this command yet.".format(arch))

    # Kernel Virtual Machine (KVM) support
    native = args.arch_native == args.deviceinfo["arch"]
    if args.qemu_kvm and native and os.path.exists("/dev/kvm"):
        command += ["-enable-kvm"]
        command += ["-cpu", "host"]
    else:
        logging.info("WARNING: QEMU is not using KVM and will run slower!")

    if args.qemu_cpu:
        command += ["-cpu", args.qemu_cpu]

    display = args.qemu_display
    if display != "none":
        display += ",gl=" + ("on" if args.qemu_gl else "off")

    command += ["-display", display]
    command += ["-show-cursor"]

    # Audio support
    if args.qemu_audio:
        command += ["-audiodev", args.qemu_audio + ",id=audio"]
        command += ["-soundhw", "hda"]

    return (command, env)


def resize_image(args, img_size_new, img_path):
    """
    Truncates an image to a specific size. The value must be larger than the
    current image size, and it must be specified in MiB or GiB units (powers of
    1024).

    :param img_size_new: new image size in M or G
    :param img_path: the path to the image
    """
    # Current image size in bytes
    img_size = os.path.getsize(img_path)

    # Make sure we have at least 1 integer followed by either M or G
    pattern = re.compile("^[0-9]+[M|G]$")
    if not pattern.match(img_size_new):
        raise RuntimeError("IMAGE_SIZE must be in [M]iB or [G]iB, e.g. 2048M"
                           " or 2G")

    # Remove M or G and convert to bytes
    img_size_new_bytes = int(img_size_new[:-1]) * 1024 * 1024

    # Convert further for G
    if (img_size_new[-1] == "G"):
        img_size_new_bytes = img_size_new_bytes * 1024

    if (img_size_new_bytes >= img_size):
        logging.info(f"Resize image to {img_size_new}: {img_path}")
        pmb.helpers.run.root(args, ["truncate", "-s", img_size_new, img_path])
    else:
        # Convert to human-readable format
        # NOTE: We convert to M here, and not G, so that we don't have to display
        # a size like 1.25G, since decimal places are not allowed by truncate.
        # We don't want users thinking they can use decimal numbers, and so in
        # this example, they would need to use a size greater then 1280M instead.
        img_size_str = str(round(img_size / 1024 / 1024)) + "M"

        raise RuntimeError(f"IMAGE_SIZE must be {img_size_str} or greater")


def sigterm_handler(number, frame):
    raise RuntimeError("pmbootstrap was terminated by another process,"
                       " and killed the QEMU VM it was running.")


def install_depends(args, arch):
    """
    Install any necessary qemu dependencies in native chroot
    """
    depends = [
        "mesa-dri-classic",
        "mesa-dri-gallium",
        "mesa-egl",
        "mesa-gl",
        "qemu",
        "qemu-audio-alsa",
        "qemu-audio-pa",
        "qemu-audio-sdl",
        "qemu-hw-display-virtio-gpu",
        "qemu-hw-display-virtio-gpu-pci",
        "qemu-hw-display-virtio-vga",
        "qemu-system-" + arch,
        "qemu-ui-gtk",
        "qemu-ui-opengl",
        "qemu-ui-sdl",
    ]

    # QEMU packaging isn't split up as much in 3.12
    channel_cfg = pmb.config.pmaports.read_config_channel(args)
    if channel_cfg["branch_aports"] == "3.12-stable":
        depends.remove("qemu-hw-display-virtio-gpu")
        depends.remove("qemu-hw-display-virtio-gpu-pci")
        depends.remove("qemu-hw-display-virtio-vga")
        depends.remove("qemu-ui-opengl")

    pmb.chroot.apk.install(args, depends)


def run(args):
    """
    Run a postmarketOS image in qemu
    """
    if not args.device.startswith("qemu-"):
        raise RuntimeError("'pmbootstrap qemu' can be only used with one of "
                           "the QEMU device packages. Run 'pmbootstrap init' "
                           "and select the 'qemu' vendor.")
    arch = pmb.parse.arch.alpine_to_qemu(args.deviceinfo["arch"])

    img_path = system_image(args)
    img_path_2nd = None
    if args.second_storage:
        img_path_2nd = create_second_storage(args)

    if not args.host_qemu:
        install_depends(args, arch)
    logging.info("Running postmarketOS in QEMU VM (" + arch + ")")

    qemu, env = command_qemu(args, arch, img_path, img_path_2nd)

    # Workaround: QEMU runs as local user and needs write permissions in the
    # rootfs, which is owned by root
    if not os.access(img_path, os.W_OK):
        pmb.helpers.run.root(args, ["chmod", "666", img_path])

    # Resize the rootfs (or show hint)
    if args.image_size:
        resize_image(args, args.image_size, img_path)
    else:
        logging.info("NOTE: Run 'pmbootstrap qemu --image-size 2G' to set"
                     " the rootfs size when you run out of space!")

    # SSH/serial hints
    logging.info("Connect to the VM:")
    logging.info("* (ssh) ssh -p {port} {user}@localhost".format(**vars(args)))
    logging.info("* (serial) in this console (stdout/stdin)")

    # Run QEMU and kill it together with pmbootstrap
    process = None
    try:
        signal.signal(signal.SIGTERM, sigterm_handler)
        process = pmb.helpers.run.user(args, qemu, output="tui", env=env)
    except KeyboardInterrupt:
        # Don't show a trace when pressing ^C
        pass
    finally:
        if process:
            process.terminate()
