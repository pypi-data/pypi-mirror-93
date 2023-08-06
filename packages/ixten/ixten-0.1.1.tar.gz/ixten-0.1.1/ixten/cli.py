################################################################################
#    Copyright 2021 @ Telefónica
#
#    This program is part of Ixten. You can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
################################################################################


import argparse
import datetime as dt
import json
import sys

from ixten.core import verify_ports
from ixten.io.preparations import generate_target_ports
from ixten.io.preparations import generate_target_ip_addresses
from ixten.utils.banner import show_banner
import ixten.utils.misc as misc


def main(argv=None):
    """The entry point for the script"""
    parser = argparse.ArgumentParser(
        "Lamming port scanner to verify active in one of your hosts is active",
        add_help=False,
    )

    source_parser = parser.add_mutually_exclusive_group(required=True)
    source_parser.add_argument(
        '-f', '--file',
        metavar='<FILE_PATH>',
        action='store',
        help="The file where the list of services is being stored."
    )

    source_parser.add_argument(
        '-i', '--ip-addresses',
        metavar='<IP_ADDRESS>',
        nargs='+',
        action='store',
        help="The list of ip addresses to monitor."
    )

    # Port options
    # ------------
    port_parser = parser.add_argument_group(
        'Port parser',
        'Ports can be provided using the number of the IP port or the typical protocol used on them.'
    )
    port_parser.add_argument(
        '-p', '--ports',
        metavar='<PORT>',
        action='store',
        nargs='+',
        default=[],
        type=int,
        help='The list of ports to monitor. Default: [].'
    )
    port_parser.add_argument(
        '-P', '--protocols',
        metavar='<PROTOCOL_NAME>',
        action='store',
        nargs='+',
        default=[],
        choices=["ssh", "http", "https", "rdp", "cobalt_strike"],
        help='The list of protocols to verify. Default ports will be used. Default: [].'
    )

    # About options
    # -------------
    group_about = parser.add_argument_group(
        'About this tool',
        'Get additional information about this package.'
    )
    group_about.add_argument(
        '-h', '--help',
        action='help',
        help='shows this help and exits.'
    )
    group_about.add_argument(
        '--version',
        action='version',
        version='%(prog)s 0.1.0',
        help='shows the version of this tool and exits.'
    )

    args = parser.parse_args(argv)

    show_banner()

    print(f"[*] Preparing the targets…")
    verifications = verify_ports(
        generate_target_ip_addresses(args),
        generate_target_ports(args)
    )

    print(f"[*] Final results:")
    print(
        misc.emphasis(
            json.dumps(
                verifications,
                indent=2,
                default=str,
                sort_keys=True
            )
        )
    )


if __name__ == '__main__':
    main(sys.argv[1:])
