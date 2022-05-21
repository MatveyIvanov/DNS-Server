from typing import Union


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