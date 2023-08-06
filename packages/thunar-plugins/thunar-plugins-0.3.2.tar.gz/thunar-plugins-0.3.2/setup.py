#!/usr/bin/env python3
import sys
import runpy
import os
import re
import itertools
import glob
import subprocess
from setuptools import setup

# TODO: This is a really bulky solution... Rather use SCons here for example.
if glob.glob("thunar_plugins/locale/*.po"):
    cmd = ["make", "-C", "thunar_plugins/locale"]
    print("Running «{}»".format(" ".join(cmd)))
    subprocess.check_output(cmd)


def get_version():
    try:
        git_version = subprocess.check_output(
            [
                "git",
                "describe",
                "--tags",
                "--match",
                "v*",
                "--always",
                "--dirty",
            ],
            stderr=subprocess.DEVNULL,
            cwd=os.path.dirname(os.path.abspath(__file__)),
        )
        d = re.fullmatch(
            pattern=r"[a-z]*(?P<tagversion>\d+(:?\.\d+)*)"
            r"(?:[^.\d]+(?P<revcount>\d+)[^.\da-z]+?(?P<commit>[a-z0-9]+))?"
            r"(?:[^.\d]+?(?P<dirty>dirty))?",
            string=git_version.decode(errors="ignore").strip(),
            flags=re.IGNORECASE,
        ).groupdict()
        return "+".join(
            filter(
                bool,
                itertools.chain(
                    (d.get("tagversion", "0"),),
                    (
                        ".".join(
                            filter(
                                bool,
                                (
                                    d[k]
                                    for k in (
                                        "revcount",
                                        "commit",
                                        "dirty",
                                    )
                                ),
                            )
                        ),
                    ),
                ),
            )
        )
    except (
        subprocess.CalledProcessError,
        OSError,
        ModuleNotFoundError,
        AttributeError,
        TypeError,
        StopIteration,
    ) as e:
        print(e)
        return None


dynamic_version = get_version()
if dynamic_version:
    version_path = os.path.join(
        os.path.dirname(__file__), "thunar_plugins", "version.py"
    )
    with open(version_path, "w") as fh:
        fh.write('__version__ = "{}"\n'.format(dynamic_version))

try:
    static_version = runpy.run_path(
        os.path.join("thunar_plugins", "version.py")
    ).get("__version__", "0+brokenversion")
except BaseException as e:
    print(e)
    static_version = "0+brokenversion"

setup(version=static_version)
