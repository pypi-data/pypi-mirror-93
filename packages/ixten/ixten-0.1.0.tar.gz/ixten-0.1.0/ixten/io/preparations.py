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


def generate_target_ports(args):
    """Creates the final list of ports based on the arguments

    Args:
        args (args): The parsed arguments

    Returns:
        set().
    """
    ports = set(args.ports)

    for protocol in args.protocols:
        if protocol == "ssh":
            ports.add(22)
        if protocol == "http":
            ports.add(80)
        if protocol == "https":
            ports.add(443)
        if protocol == "rdp":
            ports.add(3389)
        if protocol == "cobalt_strike":
            ports.add(50050)
    return ports


def generate_target_ip_addresses(args):
    """Creates the final list of ip_addresses based on the arguments

    Args:
        args (args): The parsed arguments

    Returns:
        set().
    """
    if args.file:
        with open(args.file) as input_file:
            return set(input_file.read().splitlines())
    else:
        return set(args.ip_addresses)
