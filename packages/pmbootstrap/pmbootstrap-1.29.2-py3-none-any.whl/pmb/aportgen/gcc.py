# Copyright 2021 Oliver Smith
# SPDX-License-Identifier: GPL-3.0-or-later
import pmb.aportgen.core
import pmb.helpers.git
import pmb.helpers.run


def generate(args, pkgname):
    # Copy original aport
    prefix = pkgname.split("-")[0]
    arch = pkgname.split("-")[1]
    if prefix == "gcc":
        upstream = pmb.aportgen.core.get_upstream_aport(args, "gcc")
        based_on = "main/gcc (from Alpine)"
    elif prefix == "gcc4":
        upstream = args.aports + "/main/gcc4"
        based_on = "main/gcc4 (from postmarketOS)"
    elif prefix == "gcc6":
        upstream = args.aports + "/main/gcc6"
        based_on = "main/gcc6 (from postmarketOS)"
    else:
        raise ValueError("Invalid prefix '" + prefix + "', expected gcc, gcc4 or"
                         " gcc6.")
    pmb.helpers.run.user(args, ["cp", "-r", upstream, args.work + "/aportgen"])

    # Rewrite APKBUILD (only building for native covers most use cases and
    # saves a lot of build time, can be changed on demand)
    fields = {
        "pkgname": pkgname,
        "pkgdesc": "Stage2 cross-compiler for " + arch,
        "arch": args.arch_native,
        "depends": "isl binutils-" + arch + " mpc1",
        "makedepends_build": "gcc g++ paxmark bison flex texinfo gawk zip gmp-dev mpfr-dev mpc1-dev zlib-dev",
        "makedepends_host": "linux-headers gmp-dev mpfr-dev mpc1-dev isl-dev zlib-dev musl-dev-" + arch + " binutils-" + arch,
        "subpackages": "g++-" + arch + ":gpp" if prefix == "gcc" else "",

        # gcc6: options is already there, so we need to replace it and not only
        # set it below the header like done below.
        "options": "!strip !tracedeps",

        "LIBGOMP": "false",
        "LIBGCC": "false",
        "LIBATOMIC": "false",
        "LIBITM": "false",
    }

    below_header = "CTARGET_ARCH=" + arch + """
        CTARGET="$(arch_to_hostspec ${CTARGET_ARCH})"
        LANG_D=false
        LANG_OBJC=false
        LANG_JAVA=false
        LANG_GO=false
        LANG_FORTRAN=false
        LANG_ADA=false
        options="!strip !tracedeps"

        # abuild doesn't try to tries to install "build-base-$CTARGET_ARCH"
        # when this variable matches "no*"
        BOOTSTRAP="nobuildbase"

        # abuild will only cross compile when this variable is set, but it
        # needs to find a valid package database in there for dependency
        # resolving, so we set it to /.
        CBUILDROOT="/"

        _cross_configure="--disable-bootstrap --with-sysroot=/usr/$CTARGET"
    """

    replace_simple = {
        # Do not package libstdc++, do not add "g++-$ARCH" here (already
        # did that explicitly in the subpackages variable above, so
        # pmbootstrap picks it up properly).
        '*subpackages="$subpackages libstdc++:libcxx:*': None,

        # We set the cross_configure variable at the beginning, so it does not
        # use CBUILDROOT as sysroot. In the original APKBUILD this is a local
        # variable, but we make it a global one.
        '*_cross_configure=*': None,
    }

    pmb.aportgen.core.rewrite(args, pkgname, based_on, fields,
                              replace_simple=replace_simple,
                              below_header=below_header)
