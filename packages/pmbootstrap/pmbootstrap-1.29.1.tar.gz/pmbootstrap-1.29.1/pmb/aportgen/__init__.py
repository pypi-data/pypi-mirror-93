# Copyright 2021 Oliver Smith
# SPDX-License-Identifier: GPL-3.0-or-later
import os
import logging
import pmb.aportgen.binutils
import pmb.aportgen.busybox_static
import pmb.aportgen.device
import pmb.aportgen.gcc
import pmb.aportgen.linux
import pmb.aportgen.musl
import pmb.aportgen.grub_efi
import pmb.config
import pmb.helpers.cli


def properties(pkgname):
    """
    Get the `pmb.config.aportgen` properties for the aport generator, based on
    the pkgname prefix.

    Example: "musl-armhf" => ("musl", "cross", {"confirm_overwrite": False})

    :param pkgname: package name
    :returns: (prefix, folder, options)
    """
    for folder, options in pmb.config.aportgen.items():
        for prefix in options["prefixes"]:
            if pkgname.startswith(prefix):
                return (prefix, folder, options)
    logging.info("NOTE: aportgen is for generating postmarketOS specific"
                 " aports, such as the cross-compiler related packages"
                 " or the linux kernel fork packages.")
    logging.info("NOTE: If you wanted to package new software in general, try"
                 " 'pmbootstrap newapkbuild' to generate a template.")
    raise ValueError("No generator available for " + pkgname + "!")


def generate(args, pkgname):
    if args.fork_alpine:
        prefix, folder, options = (pkgname, "temp", {"confirm_overwrite": True})
    else:
        prefix, folder, options = properties(pkgname)
    path_target = args.aports + "/" + folder + "/" + pkgname

    # Confirm overwrite
    if options["confirm_overwrite"] and os.path.exists(path_target):
        logging.warning("WARNING: Target folder already exists: " + path_target)
        if not pmb.helpers.cli.confirm(args, "Continue and overwrite?"):
            raise RuntimeError("Aborted.")

    if os.path.exists(args.work + "/aportgen"):
        pmb.helpers.run.user(args, ["rm", "-r", args.work + "/aportgen"])
    if args.fork_alpine:
        upstream = pmb.aportgen.core.get_upstream_aport(args, pkgname)
        pmb.helpers.run.user(args, ["cp", "-r", upstream, args.work + "/aportgen"])
        pmb.aportgen.core.rewrite(args, pkgname, replace_simple={"# Contributor:*": None, "# Maintainer:*": None})
    else:
        # Run pmb.aportgen.PREFIX.generate()
        getattr(pmb.aportgen, prefix.replace("-", "_")).generate(args, pkgname)

    # Move to the aports folder
    if os.path.exists(path_target):
        pmb.helpers.run.user(args, ["rm", "-r", path_target])
    pmb.helpers.run.user(
        args, ["mv", args.work + "/aportgen", path_target])

    logging.info("*** pmaport generated: " + path_target)
