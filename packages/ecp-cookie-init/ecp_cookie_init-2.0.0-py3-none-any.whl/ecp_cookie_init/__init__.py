# -*- coding: utf-8 -*-
# Copyright 2020 Cardiff University
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, see <http://www.gnu.org/licenses/>.

"""Generate an ECP cookie using CIECPLib
"""

import argparse
import sys
import warnings
from contextlib import redirect_stdout

from ciecplib import __version__ as CIECPLIB_VERSION
from ciecplib.tool.ecp_get_cookie import (
    DEFAULT_COOKIE_FILE,
    main as ecp_get_cookie,
)

__version__ = "2.0.0"


def _ecp_endpoint(dn):
    return "https://{}/idp/profile/SAML2/SOAP/ECP".format(dn)


# custom name->IdP domain name map
CUSTOM_IDPS = {
    "LIGO.ORG": ["login.ligo.org", "login2.ligo.org"],
    "LIGOGuest": ["login.guest.ligo.org"],
    "SUGWG": ["sugwg-login.phy.syr.edu"],
    "CardiffUniversity": ["idp.cf.ac.uk"],
    "TEST.LIGO.ORG": ["login-test.ligo.org"],
    "DEV.LIGO.ORG": ["login-dev.ligo.org"],
}
# make them all proper endpoint URLS to pass to ciecplib
CUSTOM_IDPS = {key: list(map(_ecp_endpoint, value)) for
               key, value in CUSTOM_IDPS.items()}


class _VersionAction(argparse._VersionAction):
    def __init__(self, *args, version=None, **kwargs):
        if version is None:
            version = "\n".join((
                "ecp-cookie-init version {}".format(__version__),
                "ciecplib version {}".format(CIECPLIB_VERSION),
            ))
        super().__init__(*args, version=version, **kwargs)


class ArgumentFormatter(
    argparse.ArgumentDefaultsHelpFormatter,
    argparse.RawDescriptionHelpFormatter,
):
    pass


def create_parser():
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=ArgumentFormatter,
        prog="ecp-cookie-init",
    )

    parser.add_argument(
        "-d",
        "--debug",
        action="store_true",
        default=False,
        help="write debug output to stdout",
    )
    parser.add_argument(
        "-v",
        "--version",
        action=_VersionAction,
        help="write version information to stdout",
    )
    parser.add_argument(
        "-i",
        "--idp-host",
        dest="idp_hosts",
        metavar="hostname",
        default=argparse.SUPPRESS,
        help="use alternative IdP host, e.g. 'login2.ligo.org'",
    )
    parser.add_argument(
        "-k",
        "--kerberos",
        action="store_true",
        default=False,
        help="enable kerberos negotiation, do not provide username",
    )
    parser.add_argument(
        "-K",
        action="store_true",
        default=False,
        help="duplicate of -k",
    )
    parser.add_argument(
        "-c",
        "--cookiefile",
        default=DEFAULT_COOKIE_FILE,
        help="use specified cookie file",
    )
    parser.add_argument(
        "-o",
        "--output-file",
        help="direct output to file",
    )
    parser.add_argument(
        "-n",
        "--no-output",
        action="store_true",
        default=False,
        help="discard all output",
    )
    parser.add_argument(
        "-X",
        "--destroy",
        action="store_true",
        default=False,
        help="destroy cookie file",
    )

    # positionals
    parser.add_argument(
        "idp_tag",
        metavar="IdP_tag",
        nargs="?",
        help="name/url of identity provider",
    )
    parser.add_argument(
        "target_url",
        help="target for cookie",
    )
    parser.add_argument(
        "username",
        metavar="login",
        nargs="?",
        help="login username (required if not using --kerberos)",
    )

    # augment parser for manpage
    parser.man_short_description = "generate an auth cookie using ECP"

    return parser


def parse_command_line(args):
    parser = create_parser()
    args = parser.parse_args(args=args)
    if (
            not args.destroy and
            not (args.kerberos or (args.idp_tag and args.username))
    ):
        parser.error("IdP_tag and login are required if not using --kerberos")
    try:  # format --idp-host argument as a list of one
        args.idp_hosts = [args.idp_hosts]
    except AttributeError:  # --idp-host not given
        try:
            args.idp_hosts = CUSTOM_IDPS[args.idp_tag]
        except KeyError:  # IdP_tag not recognised, just use what we got
            args.idp_hosts = [args.idp_tag]
    return args


def ecp_cookie_init(args=None):
    args = parse_command_line(args)

    # handle output redirection here
    if args.output_file:
        outf = open(args.output_file, "w")
    else:
        outf = sys.stdout
    try:
        with redirect_stdout(outf):
            _inner(args)
    finally:
        if args.output_file:
            outf.close()


def _inner(args):
    # map arguments
    ciecplibargs = [args.target_url]
    if args.username:
        ciecplibargs.extend(("--username", args.username))
    if args.kerberos:
        ciecplibargs.append("--kerberos")
    if args.debug and not args.no_output:
        ciecplibargs.append("--debug")
    if args.cookiefile:
        ciecplibargs.extend(("--cookiefile", args.cookiefile))

    # handle special modes
    if args.destroy:
        return ecp_get_cookie(ciecplibargs + ["--destroy"])

    # run the thing
    for idp in args.idp_hosts:
        curargs = ciecplibargs + [
            "--identity-provider", idp,
        ]
        if args.debug:
            print("Delegating call to ecp_get_cookie...")
            print("$ ecp_get_cookie {}".format(" ".join(curargs)))
        try:
            ecp_get_cookie(curargs)
        except Exception as exc:  # _all_ exceptions are caught
            if idp == args.idp_hosts[-1]:
                raise
            warnings.warn(
                "Caught {}: {}".format(type(exc).__name__, str(exc)),
            )
        else:
            return
