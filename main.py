import sys
import re
from dns_client.Client import Client
from dns_client.exceptions import ValidationError


MAX_QUERIES_TO_GET_NEW_IP = 15
MANY_FLAGS = ('-a', '--all') # If set then check for more than 1 IP


if __name__ == "__main__":
    # Get the host name from the command line.
    domain_name = ''
    many = False

    try:
        domain_name = sys.argv[1]
    except IndexError:
        print('\n\
        Domain name is required.\n\n\
        Command example: python main.py www.example.com')

        sys.exit(0)

    try:
        many = sys.argv[2]
        if many not in MANY_FLAGS:
            print("Invalid flag. If you want to get more than 1 IP, then user -a or --all flag.")

            sys.exit(0)
        many = True
    except IndexError:
        pass

    result = {
        'domain_name': None,
        'ip_addresses': set(),
        'errors': None
    }

    DNS_Client = Client()
    repeat_count = 0
    while True:
        try:
            # Send packet
            DNS_Client.send(domain_name=domain_name)
            # Recieve packet
            data = DNS_Client.recieve()
            if data['errors']:
                result = data
                break
            
            if data['ip_address'] in result['ip_addresses']:
                repeat_count += 1
                if repeat_count >= MAX_QUERIES_TO_GET_NEW_IP:
                    break
                continue
            repeat_count = 0

            if not result['domain_name']:
                result['domain_name'] = data['domain_name']
            result['ip_addresses'].add(data['ip_address'])

            if not many:
                break
        except ValidationError as e:
            print(str(e))

            sys.exit(0)

    # Check for errors
    if result['errors']:
        print(f"\n\
        There was an error while handling a dns query.\n\n\
        Error message: {result['errors']}")
    else:
        print(f"\n\
        Success!\n\n\
        Domain name: {result['domain_name']}")
        if len(result['ip_addresses']) == 1:
            print("\n\
        IP address:   --------------\n", end='')
        else:
            print("\n\
        IP addresses:   --------------\n", end='')
        for ip in result['ip_addresses']:
            print(f"\
                        {ip}")
