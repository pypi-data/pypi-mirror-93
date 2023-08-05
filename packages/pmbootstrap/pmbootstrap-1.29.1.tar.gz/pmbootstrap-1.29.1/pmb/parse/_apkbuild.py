# Copyright 2021 Oliver Smith
# SPDX-License-Identifier: GPL-3.0-or-later
import logging
import os
import re
from collections import OrderedDict

import pmb.config
import pmb.helpers.devices
import pmb.parse.version

# sh variable name regex: https://stackoverflow.com/a/2821201/3527128

# ${foo}
revar = re.compile(r"\${([a-zA-Z_]+[a-zA-Z0-9_]*)}")

# $foo
revar2 = re.compile(r"\$([a-zA-Z_]+[a-zA-Z0-9_]*)")

# ${var/foo/bar}, ${var/foo/}, ${var/foo} -- replace foo with bar
revar3 = re.compile(r"\${([a-zA-Z_]+[a-zA-Z0-9_]*)/([^/]+)(?:/([^/]*?))?}")

# ${foo#bar} -- cut off bar from foo from start of string
revar4 = re.compile(r"\${([a-zA-Z_]+[a-zA-Z0-9_]*)#(.*)}")


def replace_variable(apkbuild, value: str) -> str:
    # ${foo}
    for match in revar.finditer(value):
        try:
            logging.verbose("{}: replace '{}' with '{}'".format(
                            apkbuild["pkgname"], match.group(0),
                            apkbuild[match.group(1)]))
            value = value.replace(match.group(0), apkbuild[match.group(1)], 1)
        except KeyError:
            logging.verbose("{}: key '{}' for replacing '{}' not found, ignoring"
                            "".format(apkbuild["pkgname"], match.group(1),
                                      match.group(0)))

    # $foo
    for match in revar2.finditer(value):
        try:
            newvalue = apkbuild[match.group(1)]
            logging.verbose("{}: replace '{}' with '{}'".format(
                            apkbuild["pkgname"], match.group(0),
                            newvalue))
            value = value.replace(match.group(0), newvalue, 1)
        except KeyError:
            logging.verbose("{}: key '{}' for replacing '{}' not found, ignoring"
                            "".format(apkbuild["pkgname"], match.group(1),
                                      match.group(0)))

    # ${var/foo/bar}, ${var/foo/}, ${var/foo}
    for match in revar3.finditer(value):
        try:
            newvalue = apkbuild[match.group(1)]
            search = match.group(2)
            replacement = match.group(3)
            if replacement is None:  # arg 3 is optional
                replacement = ""
            newvalue = newvalue.replace(search, replacement, 1)
            logging.verbose("{}: replace '{}' with '{}'".format(
                            apkbuild["pkgname"], match.group(0), newvalue))
            value = value.replace(match.group(0), newvalue, 1)
        except KeyError:
            logging.verbose("{}: key '{}' for replacing '{}' not found, ignoring"
                            "".format(apkbuild["pkgname"], match.group(1),
                                      match.group(0)))

    # ${foo#bar}
    rematch4 = revar4.finditer(value)
    for match in rematch4:
        try:
            newvalue = apkbuild[match.group(1)]
            substr = match.group(2)
            if newvalue.startswith(substr):
                newvalue = newvalue.replace(substr, "", 1)
            logging.verbose("{}: replace '{}' with '{}'".format(
                            apkbuild["pkgname"], match.group(0), newvalue))
            value = value.replace(match.group(0), newvalue, 1)
        except KeyError:
            logging.verbose("{}: key '{}' for replacing '{}' not found, ignoring"
                            "".format(apkbuild["pkgname"], match.group(1),
                                      match.group(0)))

    return value


def function_body(path, func):
    """
    Get the body of a function in an APKBUILD.

    :param path: full path to the APKBUILD
    :param func: name of function to get the body of.
    :returns: function body in an array of strings.
    """
    func_body = []
    in_func = False
    lines = read_file(path)
    for line in lines:
        if in_func:
            if line.startswith("}"):
                in_func = False
                break
            func_body.append(line)
            continue
        else:
            if line.startswith(func + "() {"):
                in_func = True
                continue
    return func_body


def read_file(path):
    """
    Read an APKBUILD file

    :param path: full path to the APKBUILD
    :returns: contents of an APKBUILD as a list of strings
    """
    with open(path, encoding="utf-8") as handle:
        lines = handle.readlines()
        if handle.newlines != '\n':
            raise RuntimeError("Wrong line endings in APKBUILD: " + path)
    return lines


def parse_attribute(attribute, lines, i, path):
    """
    Parse one attribute from the APKBUILD.

    It may be written across multiple lines, use a quoting sign and/or have
    a comment at the end. Some examples:

    pkgrel=3
    options="!check" # ignore this comment
    arch='all !armhf'
    depends="
        first-pkg
        second-pkg"

    :param attribute: from the APKBUILD, i.e. "pkgname"
    :param lines: \n-terminated list of lines from the APKBUILD
    :param i: index of the line we are currently looking at
    :param path: full path to the APKBUILD (for error message)
    :returns: (found, value, i)
              found: True if the attribute was found in line i, False otherwise
              value: that was parsed from the line
              i: line that was parsed last
    """
    # Check for and cut off "attribute="
    if not lines[i].startswith(attribute + "="):
        return (False, None, i)
    value = lines[i][len(attribute + "="):-1]

    # Determine end quote sign
    end_char = None
    for char in ["'", "\""]:
        if value.startswith(char):
            end_char = char
            value = value[1:]
            break

    # Single line
    if not end_char:
        return (True, value, i)
    if end_char in value:
        value = value.split(end_char, 1)[0]
        return (True, value, i)

    # Parse lines until reaching end quote
    i += 1
    while i < len(lines):
        line = lines[i]
        value += " "
        if end_char in line:
            value += line.split(end_char, 1)[0].strip()
            return (True, value.strip(), i)
        value += line.strip()
        i += 1

    raise RuntimeError("Can't find closing quote sign (" + end_char + ") for"
                       " attribute '" + attribute + "' in: " + path)


def _parse_attributes(path, lines, apkbuild_attributes, ret):
    """
    Parse attributes from a list of lines. Variables are replaced with values
    from ret (if found) and split into the format configured in apkbuild_attributes.

    :param lines: the lines to parse
    :param apkbuild_attributes: the attributes to parse
    :param ret: a dict to update with new parsed variable
    """
    for i in range(len(lines)):
        for attribute, options in apkbuild_attributes.items():
            found, value, i = parse_attribute(attribute, lines, i, path)
            if not found:
                continue

            ret[attribute] = replace_variable(ret, value)

    if "subpackages" in apkbuild_attributes:
        subpackages = OrderedDict()
        for subpkg in ret["subpackages"].split(" "):
            if subpkg:
                _parse_subpackage(path, lines, ret, subpackages, subpkg)
        ret["subpackages"] = subpackages

    # Split attributes
    for attribute, options in apkbuild_attributes.items():
        if options.get("array", False):
            # Split up arrays, delete empty strings inside the list
            ret[attribute] = list(filter(None, ret[attribute].split(" ")))


def _parse_subpackage(path, lines, apkbuild, subpackages, subpkg):
    """
    Attempt to parse attributes from a subpackage function.
    This will attempt to locate the subpackage function in the APKBUILD and
    update the given attributes with values set in the subpackage function.

    :param path: path to APKBUILD
    :param lines: the lines to parse
    :param apkbuild: dict of attributes already parsed from APKBUILD
    :param subpackages: the subpackages dict to update
    :param subpkg: the subpackage to parse
                   (may contain subpackage function name separated by :)
    """
    subpkgparts = subpkg.split(":")
    subpkgname = subpkgparts[0]
    subpkgsplit = subpkgname[subpkgname.rfind("-") + 1:]
    if len(subpkgparts) > 1:
        subpkgsplit = subpkgparts[1]

    # Find start and end of package function
    start = end = 0
    prefix = subpkgsplit + "() {"
    for i in range(len(lines)):
        if lines[i].startswith(prefix):
            start = i + 1
        elif start and lines[i].startswith("}"):
            end = i
            break

    if not start:
        # Unable to find subpackage function in the APKBUILD.
        # The subpackage function could be actually missing, or this is a problem
        # in the parser. For now we also don't handle subpackages with default
        # functions (e.g. -dev or -doc).
        # In the future we may want to specifically handle these, and throw
        # an exception here for all other missing subpackage functions.
        subpackages[subpkgname] = None
        logging.verbose("{}: subpackage function '{}' for subpackage '{}' not found, ignoring"
                        "".format(apkbuild["pkgname"], subpkgsplit, subpkgname))
        return

    if not end:
        raise RuntimeError("Could not find end of subpackage function, no line starts"
                           " with '}' after '" + prefix + "' in " + path)

    lines = lines[start:end]
    # Strip tabs before lines in function
    lines = [line.strip() + "\n" for line in lines]

    # Copy variables
    apkbuild = apkbuild.copy()
    apkbuild["subpkgname"] = subpkgname

    # Parse relevant attributes for the subpackage
    _parse_attributes(path, lines, pmb.config.apkbuild_package_attributes, apkbuild)

    # Return only properties interesting for subpackages
    ret = {}
    for key in pmb.config.apkbuild_package_attributes:
        ret[key] = apkbuild[key]
    subpackages[subpkgname] = ret


def apkbuild(args, path, check_pkgver=True, check_pkgname=True):
    """
    Parse relevant information out of the APKBUILD file. This is not meant
    to be perfect and catch every edge case (for that, a full shell parser
    would be necessary!). Instead, it should just work with the use-cases
    covered by pmbootstrap and not take too long.
    Run 'pmbootstrap apkbuild_parse hello-world' for a full output example.

    :param path: full path to the APKBUILD
    :param check_pkgver: verify that the pkgver is valid.
    :param check_pkgname: the pkgname must match the name of the aport folder
    :returns: relevant variables from the APKBUILD. Arrays get returned as
              arrays.
    """
    # Try to get a cached result first (we assume, that the aports don't change
    # in one pmbootstrap call)
    if path in args.cache["apkbuild"]:
        return args.cache["apkbuild"][path]

    # Read the file and check line endings
    lines = read_file(path)

    # Parse all attributes from the config
    ret = {key: "" for key in pmb.config.apkbuild_attributes.keys()}
    _parse_attributes(path, lines, pmb.config.apkbuild_attributes, ret)

    # Sanity check: pkgname
    suffix = "/" + ret["pkgname"] + "/APKBUILD"
    if check_pkgname:
        if not os.path.realpath(path).endswith(suffix):
            logging.info("Folder: '" + os.path.dirname(path) + "'")
            logging.info("Pkgname: '" + ret["pkgname"] + "'")
            raise RuntimeError("The pkgname must be equal to the name of"
                               " the folder, that contains the APKBUILD!")

    # Sanity check: pkgver
    if check_pkgver:
        if "-r" in ret["pkgver"] or not pmb.parse.version.validate(ret["pkgver"]):
            logging.info("NOTE: Valid pkgvers are described here:")
            logging.info("<https://wiki.alpinelinux.org/wiki/APKBUILD_Reference#pkgver>")
            raise RuntimeError("Invalid pkgver '" + ret["pkgver"] +
                               "' in APKBUILD: " + path)

    # Fill cache
    args.cache["apkbuild"][path] = ret
    return ret


def kernels(args, device):
    """
    Get the possible kernels from a device-* APKBUILD.

    :param device: the device name, e.g. "lg-mako"
    :returns: None when the kernel is hardcoded in depends
    :returns: kernel types and their description (as read from the subpackages)
              possible types: "downstream", "stable", "mainline"
              example: {"mainline": "Mainline description",
                        "downstream": "Downstream description"}
    """
    # Read the APKBUILD
    apkbuild_path = pmb.helpers.devices.find_path(args, device, 'APKBUILD')
    if apkbuild_path is None:
        return None
    subpackages = apkbuild(args, apkbuild_path)["subpackages"]

    # Read kernels from subpackages
    ret = {}
    subpackage_prefix = "device-" + device + "-kernel-"
    for subpkgname, subpkg in subpackages.items():
        if not subpkgname.startswith(subpackage_prefix):
            continue
        if subpkg is None:
            raise RuntimeError("Cannot find subpackage function for: " + subpkgname)
        name = subpkgname[len(subpackage_prefix):]
        ret[name] = subpkg["pkgdesc"]

    # Return
    if ret:
        return ret
    return None
