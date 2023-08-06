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
        if protocol == "ftp":
            ports.add(21)
        if protocol == "ssh":
            ports.add(22)
        elif protocol == "http":
            ports.add(80)
        elif protocol == "telnet":
            ports.add(107)
        elif protocol == "sftp":
            ports.add(115)
        elif protocol == "sql":
            ports.add(118)
        elif protocol == "netbios":
            ports.add(137)
            ports.add(138)
            ports.add(139)
        elif protocol == "imap":
            ports.add(143)
            ports.add(220)
            ports.add(993)
        elif protocol == "irc":
            ports.add(194)
        elif protocol == "https":
            ports.add(443)
        elif protocol == "smtp":
            ports.add(465)
        elif protocol == "net_assistant":
            ports.add(3283)
        elif protocol == "rdp":
            ports.add(3389)
        elif protocol == "teamviewer":
            ports.add(5938)
        elif protocol == "elasticsearch":
            ports.add(9200)
        elif protocol == "mongodb":
            ports.add(27017)
        elif protocol == "logmein":
            ports.add(32976)
        elif protocol == "cobalt_strike":
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
