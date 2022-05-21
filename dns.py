import sys
import re
from dns_client.Client import Client
from dns_client.exceptions import ValidationError
from dns_client import utils


MAX_QUERIES_TO_GET_NEW_IP = 15
MAX_QUERIES = 100
MANY_FLAGS = ('-a', '--all') # If set then check for more than 1 IP
HELP_FLAGS = ('-h', '--help')


if __name__ == "__main__":
    # Get the host name from the command line.
    domain_name = ''
    many = False

    try:
        domain_name = sys.argv[1]
        if domain_name in HELP_FLAGS:
            utils.print_help()
            sys.exit(0)
    except IndexError:
        print('\n\
        Domain name is required.\n\n\
        Command example: dns www.example.com\n\
        Type dns -h(--help) for more information')

        sys.exit(0)

    try:
        flag = sys.argv[2]
        if flag in MANY_FLAGS:
            many = True
        else:
            print("Invalid flag. Type dns -h(--help) for more information.")
            sys.exit(0)
    except IndexError:
        pass

    result = {
        'domain_name': domain_name,
        'ip_addresses': set(),
        'errors': None
    }

    local_response = utils.check_local_dns_records(domain_name=domain_name)
    if local_response != '':
        result['ip_addresses'].add(local_response)
        utils.print_response(data=result)
        sys.exit(0)

    DNS_Client = Client()
    repeat_count = 0
    query_count = 0
    while query_count < MAX_QUERIES:
        try:
            query_count += 1
            # Send packet
            DNS_Client.send(domain_name=domain_name)
            # Recieve packet
            data = DNS_Client.recieve()
            if data['errors']:
                result = data
                break
            
            # IP address is same, increase repeat count, break if repeat limit reached, else continue
            if data['ip_address'] in result['ip_addresses']:
                repeat_count += 1
                if repeat_count >= MAX_QUERIES_TO_GET_NEW_IP:
                    break
                continue
            repeat_count = 0

            # Add new IP address to result
            if not result['domain_name']:
                result['domain_name'] = data['domain_name']
            result['ip_addresses'].add(data['ip_address'])

            # If -a(--all) flag is not passed, return single IP
            if not many:
                break
        except ValidationError as e:
            utils.print_errors(str(e))
            sys.exit(0)

    # Check for errors
    if result['errors']:
        utils.print_errors(errors=result['errors'])
    else:
        utils.print_response(data=result)
