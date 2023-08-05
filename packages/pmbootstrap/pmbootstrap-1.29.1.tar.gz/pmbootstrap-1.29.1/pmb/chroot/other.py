# Copyright 2021 Oliver Smith
# SPDX-License-Identifier: GPL-3.0-or-later
import os
import glob
import logging
import pmb.chroot.apk
import pmb.install


def kernel_flavors_installed(args, suffix, autoinstall=True):
    """
    Get all installed kernel flavors and make sure that there's at least one

    :param suffix: the chroot suffix, e.g. "native" or "rootfs_qemu-amd64"
    :param autoinstall: make sure that at least one kernel flavor is installed
    :returns: list of installed kernel flavors, e.g. ["postmarketos-mainline"]
    """
    # Automatically install the selected kernel
    if autoinstall:
        packages = (["device-" + args.device] +
                    pmb.install.get_kernel_package(args, args.device))
        pmb.chroot.apk.install(args, packages, suffix)

    # Find all kernels in /boot
    prefix = "vmlinuz-"
    prefix_len = len(prefix)
    pattern = args.work + "/chroot_" + suffix + "/boot/" + prefix + "*"
    ret = []
    for file in glob.glob(pattern):
        flavor = os.path.basename(file)[prefix_len:]
        if flavor[-4:] == "-dtb" or flavor[-4:] == "-mtk":
            flavor = flavor[:-4]
        ret.append(flavor)

    # Return without duplicates
    return list(set(ret))


def tempfolder(args, path, suffix="native"):
    """
    Create a temporary folder inside the chroot, that belongs to "user".
    The folder gets deleted, if it already exists.

    :param path: of the temporary folder inside the chroot
    :returns: the path
    """
    if os.path.exists(args.work + "/chroot_" + suffix + path):
        pmb.chroot.root(args, ["rm", "-r", path])
    pmb.chroot.user(args, ["mkdir", "-p", path])
    return path


def copy_xauthority(args):
    """
    Copy the host system's Xauthority file to the pmos user inside the chroot,
    so we can start X11 applications from there.
    """
    # Check $DISPLAY
    logging.info("(native) copy host Xauthority")
    if not os.environ.get("DISPLAY"):
        raise RuntimeError("Your $DISPLAY variable is not set. If you have an"
                           " X11 server running as your current user, try"
                           " 'export DISPLAY=:0' and run your last"
                           " pmbootstrap command again.")

    # Check $XAUTHORITY
    original = os.environ.get("XAUTHORITY")
    if not original:
        original = os.path.join(os.environ['HOME'], '.Xauthority')
    if not os.path.exists(original):
        raise RuntimeError("Could not find your Xauthority file, try to export"
                           " your $XAUTHORITY correctly. Looked here: " +
                           original)

    # Copy to chroot and chown
    copy = args.work + "/chroot_native/home/pmos/.Xauthority"
    if os.path.exists(copy):
        pmb.helpers.run.root(args, ["rm", copy])
    pmb.helpers.run.root(args, ["cp", original, copy])
    pmb.chroot.root(args, ["chown", "pmos:pmos", "/home/pmos/.Xauthority"])
