# Copyright 2021 Oliver Smith
# SPDX-License-Identifier: GPL-3.0-or-later
import pytest
import sys

import pmb_test  # noqa
import pmb.chroot.apk_static
import pmb.parse.apkindex
import pmb.helpers.logging
import pmb.helpers.run
import pmb.parse.bootimg


@pytest.fixture
def args(request):
    import pmb.parse
    sys.argv = ["pmbootstrap.py", "chroot"]
    args = pmb.parse.arguments()
    args.log = args.work + "/log_testsuite.txt"
    pmb.helpers.logging.init(args)
    request.addfinalizer(args.logfd.close)
    return args


def pmbootstrap_run(args, parameters, check=True):
    """Execute pmbootstrap.py with a test pmbootstrap.conf."""
    return pmb.helpers.run.user(args, ["./pmbootstrap.py"] + parameters,
                                working_dir=pmb.config.pmb_src,
                                check=check)


def test_crossdirect_rust(args):
    """ Set up buildroot_armv7 chroot for building, but remove /usr/bin/rustc.
        Build hello-world-rust for armv7, to verify that it uses
        /native/usr/bin/rustc instead of /usr/bin/rustc. The package has a
        check() function, which makes sure that the built program is actually
        working. """
    pmbootstrap_run(args, ["-y", "zap"])
    try:
        # Switch to "stable" channel, as the stable release of alpine is more
        # likely to have the same rustc version across various architectures.
        # If armv7/x86_64 have a different rustc version, this test will fail:
        # 'found crate `std` compiled by an incompatible version of rustc'
        pmb.config.pmaports.switch_to_channel_branch(args, "stable")

        pmbootstrap_run(args, ["build_init", "-barmv7"])
        pmbootstrap_run(args, ["chroot", "--add=rust", "-barmv7", "--",
                               "mv", "/usr/bin/rustc", "/usr/bin/rustc_"])
        pmbootstrap_run(args, ["build", "hello-world-rust", "--arch=armv7",
                               "--force"])
        # Make /native/usr/bin/rustc unusuable too, to make the build fail
        pmbootstrap_run(args, ["chroot", "--", "rm", "/usr/bin/rustc"])
        assert pmbootstrap_run(args, ["build", "hello-world-rust",
                                      "--arch=armv7", "--force"],
                               check=False) == 1

        # Make /usr/bin/rustc usable again, to test fallback with qemu
        pmbootstrap_run(args, ["chroot", "-barmv7", "--",
                               "mv", "/usr/bin/rustc_", "/usr/bin/rustc"])
        pmbootstrap_run(args, ["build", "hello-world-rust", "--arch=armv7",
                               "--force"])
    finally:
        # Clean up
        pmb.config.pmaports.switch_to_channel_branch(args, "edge")
        pmbootstrap_run(args, ["-y", "zap"])
