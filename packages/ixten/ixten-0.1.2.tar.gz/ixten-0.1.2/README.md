# Ixten

A simple tool to scan whether services are opened or not.

## Installation

The application needs Python 3.6+ to work and can be installed using `pip`.

```
$ pip3 install ixten
```

## Usage

```
$ ixten --help
usage: Lamming port scanner to verify active in one of your hosts is active
       (-f <FILE_PATH> | -i <IP_ADDRESS> [<IP_ADDRESS> ...])
       [-p <PORT> [<PORT> ...]] [-P <PROTOCOL_NAME> [<PROTOCOL_NAME> ...]]
       [-h] [--version]

optional arguments:
  -f <FILE_PATH>, --file <FILE_PATH>
                        The file where the list of services is being stored.
  -i <IP_ADDRESS> [<IP_ADDRESS> ...], --ip-addresses <IP_ADDRESS> [<IP_ADDRESS> ...]
                        The list of ip addresses to monitor.

Port parser:
  Ports can be provided using the number of the IP port or the typical
  protocol used on them.

  -p <PORT> [<PORT> ...], --ports <PORT> [<PORT> ...]
                        The list of ports to monitor. Default: [].
  -P <PROTOCOL_NAME> [<PROTOCOL_NAME> ...], --protocols <PROTOCOL_NAME> [<PROTOCOL_NAME> ...]
                        The list of protocols to verify. Default ports will be
                        used. Default: [].

About this tool:
  Get additional information about this package.

  -h, --help            shows this help and exits.
  --version             shows the version of this tool and exits.
```

Typical examples:

- Verify some ports in a given IP or domain (more than one IP address can be provided):

```
$ ixten -i felixbrezo.com -p 80 443 3389 9000
```

- Get IP addreses from a file:

```
$ ixten -f my_ips.txt -p 80 443 3389 9000
```

- Use protocol definition for the ports to scan:

```
$ ixten -i felixbrezo.com -P rdp https
```
