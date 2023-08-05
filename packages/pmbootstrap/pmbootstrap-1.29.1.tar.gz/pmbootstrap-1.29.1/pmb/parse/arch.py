# Copyright 2021 Oliver Smith
# SPDX-License-Identifier: GPL-3.0-or-later
import platform
import fnmatch


def alpine_native():
    machine = platform.machine()
    ret = ""

    mapping = {
        "i686": "x86",
        "x86_64": "x86_64",
        "aarch64": "aarch64",
        "armv6l": "armhf",
        "armv7l": "armv7"
    }
    if machine in mapping:
        return mapping[machine]
    raise ValueError("Can not map platform.machine '" + machine + "'"
                     " to the right Alpine Linux architecture")
    return ret


def from_chroot_suffix(args, suffix):
    if suffix == "native":
        return args.arch_native
    if suffix in [f"rootfs_{args.device}", f"installer_{args.device}"]:
        return args.deviceinfo["arch"]
    if suffix.startswith("buildroot_"):
        return suffix.split("_", 1)[1]

    raise ValueError("Invalid chroot suffix: " + suffix +
                     " (wrong device chosen in 'init' step?)")


def alpine_to_qemu(arch):
    """
    Convert the architecture to the string used in the QEMU packaging.
    """

    mapping = {
        "x86": "i386",
        "x86_64": "x86_64",
        "armhf": "arm",
        "armv7": "arm",
        "aarch64": "aarch64",
    }
    for pattern, arch_qemu in mapping.items():
        if fnmatch.fnmatch(arch, pattern):
            return arch_qemu
    raise ValueError("Can not map Alpine architecture '" + arch + "'"
                     " to the right Debian architecture.")


def alpine_to_kernel(arch):
    """
    Convert the architecture to the string used inside the kernel sources.
    You can read the mapping from the linux-vanilla APKBUILD for example.
    """
    mapping = {
        "aarch64*": "arm64",
        "arm*": "arm",
        "ppc*": "powerpc",
        "s390*": "s390"
    }
    for pattern, arch_kernel in mapping.items():
        if fnmatch.fnmatch(arch, pattern):
            return arch_kernel
    return arch


def alpine_to_hostspec(arch):
    """
    See: abuild source code/functions.sh.in: arch_to_hostspec()
    """
    mapping = {
        "aarch64": "aarch64-alpine-linux-musl",
        "armel": "armv5-alpine-linux-musleabi",
        "armhf": "armv6-alpine-linux-musleabihf",
        "armv7": "armv7-alpine-linux-musleabihf",
        "mips": "mips-alpine-linux-musl",
        "mips64": "mips64-alpine-linux-musl",
        "mipsel": "mipsel-alpine-linux-musl",
        "mips64el": "mips64el-alpine-linux-musl",
        "ppc": "powerpc-alpine-linux-musl",
        "ppc64": "powerpc64-alpine-linux-musl",
        "ppc64le": "powerpc64le-alpine-linux-musl",
        "s390x": "s390x-alpine-linux-musl",
        "x86": "i586-alpine-linux-musl",
        "x86_64": "x86_64-alpine-linux-musl",
    }
    if arch in mapping:
        return mapping[arch]

    raise ValueError("Can not map Alpine architecture '" + arch + "'"
                     " to the right hostspec value")


def cpu_emulation_required(args, arch):
    # Obvious case: host arch is target arch
    if args.arch_native == arch:
        return False

    # Other cases: host arch on the left, target archs on the right
    not_required = {
        "x86_64": ["x86"],
        "armv7": ["armel", "armhf"],
        "aarch64": ["armel", "armhf", "armv7"],
    }
    if args.arch_native in not_required:
        if arch in not_required[args.arch_native]:
            return False

    # No match: then it's required
    return True
