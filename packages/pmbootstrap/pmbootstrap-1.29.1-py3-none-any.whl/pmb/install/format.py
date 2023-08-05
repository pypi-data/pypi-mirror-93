# Copyright 2021 Oliver Smith
# SPDX-License-Identifier: GPL-3.0-or-later
import os
import logging
import pmb.chroot


def format_and_mount_boot(args, boot_label):
    """
    :param boot_label: label of the root partition (e.g. "pmOS_boot")

    When adjusting this function, make sure to also adjust
    ondev-prepare-internal-storage.sh in postmarketos-ondev.git!
    """
    mountpoint = "/mnt/install/boot"
    device = "/dev/installp1"
    filesystem = args.deviceinfo["boot_filesystem"] or "ext2"
    logging.info(f"(native) format {device} (boot, {filesystem}), mount to"
                 " mountpoint")
    if filesystem == "fat16":
        pmb.chroot.root(args, ["mkfs.fat", "-F", "16", "-n", boot_label,
                               device])
    elif filesystem == "fat32":
        pmb.chroot.root(args, ["mkfs.fat", "-F", "32", "-n", boot_label,
                               device])
    elif filesystem == "ext2":
        pmb.chroot.root(args, ["mkfs.ext2", "-F", "-q", "-L", boot_label,
                               device])
    else:
        raise RuntimeError("Filesystem " + filesystem + " is not supported!")
    pmb.chroot.root(args, ["mkdir", "-p", mountpoint])
    pmb.chroot.root(args, ["mount", device, mountpoint])


def format_luks_root(args, device):
    """
    :param device: root partition on install block device (e.g. /dev/installp2)
    """
    mountpoint = "/dev/mapper/pm_crypt"

    logging.info(f"(native) format {device} (root, luks), mount to"
                 f" {mountpoint}")
    logging.info(" *** TYPE IN THE FULL DISK ENCRYPTION PASSWORD (TWICE!) ***")

    # Avoid cryptsetup warning about missing locking directory
    pmb.chroot.root(args, ["mkdir", "-p", "/run/cryptsetup"])

    pmb.chroot.root(args, ["cryptsetup", "luksFormat",
                           "-q",
                           "--cipher", args.cipher,
                           "--iter-time", args.iter_time,
                           "--use-random",
                           device], output="interactive")
    pmb.chroot.root(args, ["cryptsetup", "luksOpen", device, "pm_crypt"],
                    output="interactive")

    if not os.path.exists(f"{args.work}/chroot_native/{mountpoint}"):
        raise RuntimeError("Failed to open cryptdevice!")


def format_and_mount_root(args, device, root_label, sdcard):
    """
    :param device: root partition on install block device (e.g. /dev/installp2)
    :param root_label: label of the root partition (e.g. "pmOS_root")
    :param sdcard: path to sdcard device (e.g. /dev/mmcblk0) or None
    """
    # Format
    if not args.rsync:
        logging.info("(native) format " + device)
        # Some downstream kernels don't support metadata_csum (#1364).
        # When changing the options of mkfs.ext4, also change them in the
        # recovery zip code (see 'grep -r mkfs\.ext4')!
        mkfs_ext4_args = ["mkfs.ext4", "-O", "^metadata_csum", "-F",
                          "-q", "-L", root_label]

        # When we don't know the file system size before hand like
        # with non-block devices, we need to explicitely set a number of
        # inodes. See #1717 and #1845 for details
        if not sdcard:
            mkfs_ext4_args = mkfs_ext4_args + ["-N", "100000"]

        pmb.chroot.root(args, mkfs_ext4_args + [device])

    # Mount
    mountpoint = "/mnt/install"
    logging.info("(native) mount " + device + " to " + mountpoint)
    pmb.chroot.root(args, ["mkdir", "-p", mountpoint])
    pmb.chroot.root(args, ["mount", device, mountpoint])


def format(args, size_reserve, boot_label, root_label, sdcard):
    """
    :param size_reserve: empty partition between root and boot in MiB (pma#463)
    :param boot_label: label of the boot partition (e.g. "pmOS_boot")
    :param root_label: label of the root partition (e.g. "pmOS_root")
    :param sdcard: path to sdcard device (e.g. /dev/mmcblk0) or None
    """
    root_dev = "/dev/installp3" if size_reserve else "/dev/installp2"

    if args.full_disk_encryption:
        format_luks_root(args, root_dev)
        root_dev = "/dev/mapper/pm_crypt"

    format_and_mount_root(args, root_dev, root_label, sdcard)
    format_and_mount_boot(args, boot_label)
