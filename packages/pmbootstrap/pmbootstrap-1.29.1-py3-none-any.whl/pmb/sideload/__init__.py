# Copyright 2021 Martijn Braam
# SPDX-License-Identifier: GPL-3.0-or-later
import glob
import os
import logging

import pmb.helpers.run
import pmb.parse.apkindex
import pmb.config.pmaports
import pmb.build


def scp_abuild_key(args, user, host):
    """ Copy the building key of the local installation to the target device,
        so it trusts the apks that were signed here.
        :param user: target device ssh username
        :param host: target device ssh hostname """

    keys = glob.glob(os.path.join(args.work, "config_abuild", "*.pub"))
    key = keys[0]
    key_name = os.path.basename(key)

    logging.info(f"Copying signing key ({key_name}) to {user}@{host}")
    command = ['scp', key, f'{user}@{host}:/tmp']
    pmb.helpers.run.user(args, command, output="interactive")

    logging.info(f"Installing signing key at {user}@{host}")
    keyname = os.path.join("/tmp", os.path.basename(key))
    remote_cmd = ['sudo', '-p', pmb.config.sideload_sudo_prompt,
                  '-S', 'mv', '-n', keyname, "/etc/apk/keys/"]
    remote_cmd = pmb.helpers.run.flat_cmd(remote_cmd)
    command = ['ssh', '-t', f'{user}@{host}', remote_cmd]
    pmb.helpers.run.user(args, command, output="tui")


def ssh_install_apks(args, user, host, paths):
    """ Copy binary packages via SCP and install them via SSH.
        :param user: target device ssh username
        :param host: target device ssh hostname
        :param paths: list of absolute paths to locally stored apks
        :type paths: list """

    remote_paths = []
    for path in paths:
        remote_paths.append(os.path.join('/tmp', os.path.basename(path)))

    logging.info(f"Copying packages to {user}@{host}")
    command = ['scp'] + paths + [f'{user}@{host}:/tmp']
    pmb.helpers.run.user(args, command, output="interactive")

    logging.info(f"Installing packages at {user}@{host}")
    add_cmd = ['sudo', '-p', pmb.config.sideload_sudo_prompt,
               '-S', 'apk', 'add'] + remote_paths
    add_cmd = pmb.helpers.run.flat_cmd(add_cmd)
    clean_cmd = pmb.helpers.run.flat_cmd(['rm'] + remote_paths)
    command = ['ssh', '-t', f'{user}@{host}', f'{add_cmd}; {clean_cmd}']
    pmb.helpers.run.user(args, command, output="tui")


def sideload(args, user, host, arch, copy_key, pkgnames):
    """ Build packages if necessary and install them via SSH.

        :param user: target device ssh username
        :param host: target device ssh hostname
        :param arch: target device architecture
        :param copy_key: copy the abuild key too
        :param pkgnames: list of pkgnames to be built """

    paths = []
    channel = pmb.config.pmaports.read_config(args)["channel"]

    for pkgname in pkgnames:
        data_repo = pmb.parse.apkindex.package(args, pkgname, arch, True)
        apk_file = f"{pkgname}-{data_repo['version']}.apk"
        host_path = os.path.join(args.work, "packages", channel, arch,
                                 apk_file)
        if not os.path.isfile(host_path):
            pmb.build.package(args, pkgname, arch, force=True)

        if not os.path.isfile(host_path):
            raise RuntimeError(f"The package '{pkgname}' could not be built")

        paths.append(host_path)

    if copy_key:
        scp_abuild_key(args, user, host)

    ssh_install_apks(args, user, host, paths)
