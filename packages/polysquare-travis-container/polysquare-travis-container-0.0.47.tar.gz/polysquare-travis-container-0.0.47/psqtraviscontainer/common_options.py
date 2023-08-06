# /psqtraviscontainer/common_options.py
#
# Options common to both both commands.
#
# See /LICENCE.md for Copyright information
"""Options common to both both commands."""

import argparse

import os

import platform

from psqtraviscontainer import architecture
from psqtraviscontainer import distro


def get_parser(action):
    """Get a parser with options common to both commands."""
    # Iterate over the available_distributions and get a list of available
    # distributions and architectures for the --distro and --arch arguments
    architectures = set()
    distributions = set()

    for config in distro.available_distributions():
        if "distro" in config:
            distributions.add(config["distro"])
        if "arch" in config:
            architectures.add(architecture.Alias.universal(config["arch"]))

    description = """{0} a CI container""".format(action)
    parser = argparse.ArgumentParser(description=description)

    current_arch = architecture.Alias.universal(platform.machine())

    parser.add_argument("containerdir",
                        metavar=("CONTAINER_DIRECTORY"),
                        help="""Directory to place container in""",
                        type=str)
    parser.add_argument("--distro",
                        type=str,
                        help="""Distribution name to create container of""",
                        choices=distributions,
                        default=os.environ.get("CONTAINER_DISTRO", None))
    parser.add_argument("--release",
                        type=str,
                        help="""Distribution release to create container of""",
                        default=os.environ.get("CONTAINER_RELEASE", None))
    parser.add_argument("--arch",
                        type=str,
                        help=("""Architecture (all architectures other """
                              """than the system architecture will be """
                              """emulated with qemu)"""),
                        choices=architectures,
                        default=os.environ.get("CONTAINER_ARCH", current_arch))
    parser.add_argument("--local",
                        action="store_true",
                        help="""Use the 'local' version of this container.""")

    return parser
