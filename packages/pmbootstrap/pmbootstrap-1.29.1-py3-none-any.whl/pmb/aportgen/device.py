# Copyright 2021 Oliver Smith
# SPDX-License-Identifier: GPL-3.0-or-later
import logging
import os
import pmb.helpers.cli
import pmb.helpers.run
import pmb.aportgen.core
import pmb.parse.apkindex
import pmb.parse.bootimg


def ask_for_architecture(args):
    architectures = pmb.config.build_device_architectures
    while True:
        ret = pmb.helpers.cli.ask(args, "Device architecture", architectures,
                                  architectures[0])
        if ret in architectures:
            return ret
        logging.fatal("ERROR: Invalid architecture specified. If you want to"
                      " add a new architecture, edit"
                      " build_device_architectures in"
                      " pmb/config/__init__.py.")


def ask_for_manufacturer(args):
    logging.info("Who produced the device (e.g. LG)?")
    return pmb.helpers.cli.ask(args, "Manufacturer", None, None, False)


def ask_for_name(args, manufacturer):
    logging.info("What is the official name (e.g. Google Nexus 5)?")
    ret = pmb.helpers.cli.ask(args, "Name", None, None, False)

    # Always add the manufacturer
    if not ret.startswith(manufacturer) and \
            not ret.startswith("Google"):
        ret = manufacturer + " " + ret
    return ret


def ask_for_year(args):
    # Regex from https://stackoverflow.com/a/12240826
    logging.info("In what year was the device released (e.g. 2012)?")
    return pmb.helpers.cli.ask(args, "Year", None, None, False,
                               validation_regex=r'^[1-9]\d{3,}$')


def ask_for_chassis(args):
    types = pmb.config.deviceinfo_chassis_types

    logging.info("What type of device is it?")
    logging.info("Valid types are: " + ", ".join(types))
    return pmb.helpers.cli.ask(args, "Chassis", None, None, True,
                               validation_regex='|'.join(types),
                               complete=types)


def ask_for_keyboard(args):
    return pmb.helpers.cli.confirm(args, "Does the device have a hardware"
                                   " keyboard?")


def ask_for_external_storage(args):
    return pmb.helpers.cli.confirm(args, "Does the device have a sdcard or"
                                   " other external storage medium?")


def ask_for_flash_method(args):
    while True:
        logging.info("Which flash method does the device support?")
        method = pmb.helpers.cli.ask(args, "Flash method",
                                     pmb.config.flash_methods,
                                     pmb.config.flash_methods[0])

        if method in pmb.config.flash_methods:
            if method == "heimdall":
                heimdall_types = ["isorec", "bootimg"]
                while True:
                    logging.info("Does the device use the \"isolated"
                                 " recovery\" or boot.img?")
                    logging.info("<https://wiki.postmarketos.org/wiki"
                                 "/Deviceinfo_flash_methods#Isorec_or_bootimg"
                                 ".3F>")
                    heimdall_type = pmb.helpers.cli.ask(args, "Type",
                                                        heimdall_types,
                                                        heimdall_types[0])
                    if heimdall_type in heimdall_types:
                        method += "-" + heimdall_type
                        break
                    logging.fatal("ERROR: Invalid type specified.")
            return method

        logging.fatal("ERROR: Invalid flash method specified. If you want to"
                      " add a new flash method, edit flash_methods in"
                      " pmb/config/__init__.py.")


def ask_for_bootimg(args):
    logging.info("You can analyze a known working boot.img file to"
                 " automatically fill out the flasher information for your"
                 " deviceinfo file. Either specify the path to an image or"
                 " press return to skip this step (you can do it later with"
                 " 'pmbootstrap bootimg_analyze').")

    while True:
        response = pmb.helpers.cli.ask(args, "Path", None, "", False)
        path = os.path.expanduser(response)
        if not path:
            return None
        try:
            return pmb.parse.bootimg(args, path)
        except Exception as e:
            logging.fatal("ERROR: " + str(e) + ". Please try again.")


def generate_deviceinfo_fastboot_content(args, bootimg=None):
    if bootimg is None:
        bootimg = {"cmdline": "",
                   "qcdt": "false",
                   "mtk_mkimage": "false",
                   "dtb_second": "false",
                   "base": "",
                   "kernel_offset": "",
                   "ramdisk_offset": "",
                   "second_offset": "",
                   "tags_offset": "",
                   "pagesize": "2048"}
    return f"""\
        deviceinfo_kernel_cmdline="{bootimg["cmdline"]}"
        deviceinfo_generate_bootimg="true"
        deviceinfo_bootimg_qcdt="{bootimg["qcdt"]}"
        deviceinfo_bootimg_mtk_mkimage="{bootimg["mtk_mkimage"]}"
        deviceinfo_bootimg_dtb_second="{bootimg["dtb_second"]}"
        deviceinfo_flash_offset_base="{bootimg["base"]}"
        deviceinfo_flash_offset_kernel="{bootimg["kernel_offset"]}"
        deviceinfo_flash_offset_ramdisk="{bootimg["ramdisk_offset"]}"
        deviceinfo_flash_offset_second="{bootimg["second_offset"]}"
        deviceinfo_flash_offset_tags="{bootimg["tags_offset"]}"
        deviceinfo_flash_pagesize="{bootimg["pagesize"]}"
        """


def generate_deviceinfo(args, pkgname, name, manufacturer, year, arch,
                        chassis, has_keyboard, has_external_storage,
                        flash_method, bootimg=None):
    codename = "-".join(pkgname.split("-")[1:])
    external_storage = "true" if has_external_storage else "false"
    # Note: New variables must be added to pmb/config/__init__.py as well
    content = f"""\
        # Reference: <https://postmarketos.org/deviceinfo>
        # Please use double quotes only. You can source this file in shell
        # scripts.

        deviceinfo_format_version="0"
        deviceinfo_name="{name}"
        deviceinfo_manufacturer="{manufacturer}"
        deviceinfo_codename="{codename}"
        deviceinfo_year="{year}"
        deviceinfo_dtb=""
        deviceinfo_modules_initfs=""
        deviceinfo_arch="{arch}"

        # Device related
        deviceinfo_chassis="{chassis}"
        deviceinfo_keyboard="{"true" if has_keyboard else "false"}"
        deviceinfo_external_storage="{external_storage}"
        deviceinfo_screen_width="800"
        deviceinfo_screen_height="600"

        # Bootloader related
        deviceinfo_flash_method="{flash_method}"
        """

    content_heimdall_bootimg = """\
        deviceinfo_flash_heimdall_partition_kernel=""
        deviceinfo_flash_heimdall_partition_system=""
        """

    content_heimdall_isorec = """\
        deviceinfo_flash_heimdall_partition_kernel=""
        deviceinfo_flash_heimdall_partition_initfs=""
        deviceinfo_flash_heimdall_partition_system=""
        """

    content_0xffff = """\
        deviceinfo_generate_legacy_uboot_initfs="true"
        """

    content_uuu = """\
        deviceinfo_generate_legacy_uboot_initfs="true"
        """

    if flash_method == "fastboot":
        content += generate_deviceinfo_fastboot_content(args, bootimg)
    elif flash_method == "heimdall-bootimg":
        content += generate_deviceinfo_fastboot_content(args, bootimg)
        content += content_heimdall_bootimg
    elif flash_method == "heimdall-isorec":
        content += content_heimdall_isorec
    elif flash_method == "0xffff":
        content += content_0xffff
    elif flash_method == "uuu":
        content += content_uuu

    # Write to file
    pmb.helpers.run.user(args, ["mkdir", "-p", args.work + "/aportgen"])
    path = args.work + "/aportgen/deviceinfo"
    with open(path, "w", encoding="utf-8") as handle:
        for line in content.rstrip().split("\n"):
            handle.write(line.lstrip() + "\n")


def generate_apkbuild(args, pkgname, name, arch, flash_method):
    # Dependencies
    depends = "postmarketos-base linux-" + "-".join(pkgname.split("-")[1:])
    if flash_method in ["fastboot", "heimdall-bootimg"]:
        depends += " mkbootimg"
    if flash_method == "0xffff":
        depends += " uboot-tools"
    depends += " mesa-dri-gallium"

    # Whole APKBUILD
    content = f"""\
        # Reference: <https://postmarketos.org/devicepkg>
        pkgname={pkgname}
        pkgdesc="{name}"
        pkgver=0.1
        pkgrel=0
        url="https://postmarketos.org"
        license="MIT"
        arch="{arch}"
        options="!check !archcheck"
        depends="{depends}"
        makedepends="devicepkg-dev"
        source="deviceinfo"

        build() {{
            devicepkg_build $startdir $pkgname
        }}

        package() {{
            devicepkg_package $startdir $pkgname
        }}

        sha512sums="(run 'pmbootstrap checksum {pkgname}' to fill)"
        """

    # Write the file
    pmb.helpers.run.user(args, ["mkdir", "-p", args.work + "/aportgen"])
    path = args.work + "/aportgen/APKBUILD"
    with open(path, "w", encoding="utf-8") as handle:
        for line in content.rstrip().split("\n"):
            handle.write(line[8:].replace(" " * 4, "\t") + "\n")


def generate(args, pkgname):
    arch = ask_for_architecture(args)
    manufacturer = ask_for_manufacturer(args)
    name = ask_for_name(args, manufacturer)
    year = ask_for_year(args)
    chassis = ask_for_chassis(args)
    has_keyboard = ask_for_keyboard(args)
    has_external_storage = ask_for_external_storage(args)
    flash_method = ask_for_flash_method(args)
    bootimg = None
    if flash_method in ["fastboot", "heimdall-bootimg"]:
        bootimg = ask_for_bootimg(args)

    generate_deviceinfo(args, pkgname, name, manufacturer, year, arch,
                        chassis, has_keyboard, has_external_storage,
                        flash_method, bootimg)
    generate_apkbuild(args, pkgname, name, arch, flash_method)
