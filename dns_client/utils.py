from typing import Union
from pathlib import Path


HOME_PATH = Path.home()
DNS_FOLDER = '.local-dns'
DNS_FILE = '.local-dns-records.txt'
DNS_LOCAL_DATA = {
    'localhost': '127.0.0.1',
    '::1': '127.0.0.1'
}

def to_hex_string(value: Union[str, int]) -> str:
    """
    Encodes either a positive integer or string to its hexadecimal representation.
    """

    result = '0'

    if value.__class__.__name__ == 'int' and value >= 0:
        result = hex(value)

        if value < 16:
            result = '0' + result[2:]

    elif value.__class__.__name__ == 'str':
        result = ''.join([hex(ord(symbol))[2:] for symbol in value])

    return '0x' + result


def print_help():
    print('\n\
        dns cli can help you get the IP address(es) for the provided domain name\n\n\
        Usage: dns <domain_name> [-a(--all)]\n\n\
        Available flags: -a(--all) - checks for multiple IP addresses for the provided domain name\
    ')

def print_errors(errors: str) -> None:
    print(f"\n\
        There was an error while handling a dns query.\n\n\
        Error message: {errors}")

def print_response(data: dict) -> None:
    ip_text = 'IP address:'
    if len(data['ip_addresses']) > 1:
        ip_text = 'IP addresses:'
        
    ip_addresses = f'{data["ip_addresses"].pop()}\n                      '
    ip_addresses += '\n                      '.join(data["ip_addresses"])

    print(f"\
        Success!\n\
        Domain name: {data['domain_name']}\n\
        {ip_text} {ip_addresses}")

def check_local_dns_records(domain_name: str) -> str:
    try:
        # Create dns folder if it does not exist
        if not Path(HOME_PATH / DNS_FOLDER).is_dir():
            _create_dns_folder()

        if not Path(HOME_PATH / DNS_FOLDER / DNS_FILE).is_file():
            _create_dns_file()

        # Read file info and check if domain_name in it
        with Path(HOME_PATH / DNS_FOLDER / DNS_FILE).open('r') as f:
            data = f.readlines()
            for line in data:
                line = line.strip(' ')
                if line.startswith('#'):
                    continue
                domain, address = line.split(' ')
                if domain == domain_name:
                    return address
    except Exception:
        pass

    return ''

def _create_dns_folder() -> None:
    Path(HOME_PATH / DNS_FOLDER).mkdir(exist_ok=True)

def _create_dns_file() -> None:
    Path(HOME_PATH / DNS_FOLDER / DNS_FILE).touch(exist_ok=True)
    __fill_dns_file()

def __fill_dns_file() -> None:
    with Path(HOME_PATH / DNS_FOLDER / DNS_FILE).open('w') as f:
        f.write("# Add your own DNS records. DNS record format: '<domain_name> <ip_address>'.\n")
        f.write("# Note that there should be a newline right after <ip_address> and exactly 1 space between <domain_name> and <ip_address>.\n")
        f.write("# The best practice would be to use below records as the examples for your own ones.\n")
        f.write("# Lines starting with '#' will be ignored.\n")
        for key, value in DNS_LOCAL_DATA.items():
            f.write(f"{key} {value}\n")
