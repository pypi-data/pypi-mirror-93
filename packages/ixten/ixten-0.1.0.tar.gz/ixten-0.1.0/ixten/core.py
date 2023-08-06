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

import datetime as dt
import socket

import ixten.utils.misc as misc


def is_open(ip, port):
    """Verify if the service answers at the given port

    Args:
        ip (str): The IP address of the service to verify.
        port (str): The service port to verify.

    Returns:
        bool."""
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(3)
    try:
        s.connect((ip, int(port)))
        s.shutdown(2)
        s.close()
        print(f"\t- {ip}:{port} --> {misc.success('Opened (✔)')}")
        return True
    except:
        print(f"\t- {ip}:{port} --> {misc.error('Closed (𐄂)')}")
        return False


def verify_ports(ips, ports):
    """Verify if the service answers at the given port

    Args:
        ip (list): The list of IP addresses of the services to verify.
        port (list): The service ports to verify.

    Returns:
        dict. The results are grouped by IP Address and port.
        {
            "date": "20210203…",
            "targets": {
                "1.1.1.1": {
                    "opened_count": 2,
                    "closed_count": 1,
                    "statuses": {
                        80: True,
                        443: True,
                        3389: False
                    }
                },
                "2.2.2.2": {
                    "opened_count": 1,
                    "closed_count": 0,
                    "statuses": {
                        80: True,
                    }
                    80: True
                }
            }
        }
        """
    results = {
        "date": str(dt.datetime.utcnow()),
        "targets": {}
    }

    for ip in ips:
        print(f"\n[*] Verifying ports at {ip}…")
        results["targets"][ip] = {
            "opened_count": 0,
            "closed_count": 0,
            "statuses": {}
        }
        for port in ports:
            if is_open(ip, port):
                results["targets"][ip]["statuses"][port] = True
                results["targets"][ip]["opened_count"] += 1
            else:
                results["targets"][ip]["statuses"][port] = False
                results["targets"][ip]["closed_count"] += 1
        print(f"[*] Results for {ip}: {misc.success(results['targets'][ip]['opened_count'])} opened and {misc.error(results['targets'][ip]['closed_count'])} closed.\n")
    return results
