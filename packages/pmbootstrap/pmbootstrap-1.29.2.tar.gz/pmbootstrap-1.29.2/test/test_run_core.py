# Copyright 2021 Oliver Smith
# SPDX-License-Identifier: GPL-3.0-or-later
""" Test pmb.helpers.run_core """
import sys
import subprocess
import pytest

import pmb_test  # noqa
import pmb.helpers.run_core


@pytest.fixture
def args(request):
    import pmb.parse
    sys.argv = ["pmbootstrap.py", "chroot"]
    args = pmb.parse.arguments()
    args.log = args.work + "/log_testsuite.txt"
    pmb.helpers.logging.init(args)
    request.addfinalizer(args.logfd.close)
    return args


def test_sanity_checks():
    func = pmb.helpers.run_core.sanity_checks

    # Invalid output
    with pytest.raises(RuntimeError) as e:
        func("invalid-output")
    assert str(e.value).startswith("Invalid output value")

    # Background and check
    func("background", check=None)
    for check in [True, False]:
        with pytest.raises(RuntimeError) as e:
            func("background", check=check)
        assert str(e.value).startswith("Can't use check with")

    # output_return
    func("log", output_return=True)
    with pytest.raises(RuntimeError) as e:
        func("tui", output_return=True)
    assert str(e.value).startswith("Can't use output_return with")


def test_background(args):
    # Sleep in background
    process = pmb.helpers.run_core.background(args, ["sleep", "1"], "/")

    # Check if it is still running
    assert process.poll() is None


def test_pipe(args):
    # Sleep in background
    process = pmb.helpers.run_core.pipe(args, ["sleep", "1"], "/")

    # Check if it is still running
    assert process.poll() is None

    # Print output in background
    process = pmb.helpers.run_core.pipe(args, ["echo", "-n", "hello"], "/")

    # Read output
    assert process.communicate()[0].decode('utf-8') == "hello"


def test_foreground_pipe(args):
    func = pmb.helpers.run_core.foreground_pipe
    cmd = ["echo", "test"]

    # Normal run
    assert func(args, cmd) == (0, "")

    # Return output
    assert func(args, cmd, output_return=True) == (0, "test\n")

    # Kill with output timeout
    cmd = ["sh", "-c", "echo first; sleep 2; echo second"]
    args.timeout = 0.3
    ret = func(args, cmd, output_return=True, output_timeout=True)
    assert ret == (-9, "first\n")

    # Kill with output timeout as root
    cmd = ["sudo", "sh", "-c", "printf first; sleep 2; printf second"]
    args.timeout = 0.3
    ret = func(args, cmd, output_return=True, output_timeout=True,
               sudo=True)
    assert ret == (-9, "first")

    # Finish before timeout
    cmd = ["sh", "-c", "echo first; sleep 0.1; echo second; sleep 0.1;"
           "echo third; sleep 0.1; echo fourth"]
    args.timeout = 0.2
    ret = func(args, cmd, output_return=True, output_timeout=True)
    assert ret == (0, "first\nsecond\nthird\nfourth\n")

    # Check if all child processes are killed after timeout.
    # The first command uses ps to get its process group id (pgid) and echo it
    # to stdout. All of the test commands will be running under that pgid.
    cmd = ["sudo", "sh", "-c",
           "pgid=$(ps -p ${1:-$$} -o pgid=);echo $pgid | tr -d '\n';" +
           "sleep 10 | sleep 20 | sleep 30"]
    args.timeout = 0.3
    ret = func(args, cmd, output_return=True, output_timeout=True,
               sudo=True)
    pgid = str(ret[1])

    cmd = ["ps", "-e", "-o", "pgid=,comm=", "--noheaders"]
    ret = subprocess.run(cmd, check=True, stdout=subprocess.PIPE)
    procs = str(ret.stdout.decode("utf-8")).rstrip().split('\n')
    child_procs = []
    for process in procs:
        items = process.split(maxsplit=1)
        if len(items) != 2:
            continue
        if pgid == items[0] and "sleep" in items[1]:
            child_procs.append(items)
    assert len(child_procs) == 0


def test_foreground_tui():
    func = pmb.helpers.run_core.foreground_tui
    assert func(["echo", "test"]) == 0


def test_core(args):
    # Background
    func = pmb.helpers.run_core.core
    msg = "test"
    process = func(args, msg, ["sleep", "1"], output="background")
    assert process.poll() is None

    # Foreground (TUI)
    ret = func(args, msg, ["echo", "test"], output="tui")
    assert ret == 0

    # Foreground (pipe)
    ret = func(args, msg, ["echo", "test"], output="log")
    assert ret == 0

    # Return output
    ret = func(args, msg, ["echo", "test"], output="log", output_return=True)
    assert ret == "test\n"

    # Check the return code
    with pytest.raises(RuntimeError) as e:
        func(args, msg, ["false"], output="log")
    assert str(e.value).startswith("Command failed:")

    # Kill with timeout
    args.timeout = 0.2
    with pytest.raises(RuntimeError) as e:
        func(args, msg, ["sleep", "1"], output="log")
    assert str(e.value).startswith("Command failed:")
