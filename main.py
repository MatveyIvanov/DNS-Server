import sys
from dns_client.Client import Client
from dns_client.exceptions import ValidationError


if __name__ == "__main__":
    # Get the host name from the command line.
    domain_name = ''

    try:
        domain_name = sys.argv[1]
    except IndexError:
        print('Domain name is required.\n \
            Command example: python main.py www.example.com')

        sys.exit(0)

    DNS_Client = Client()
    try:
        # Send packet
        DNS_Client.send(domain_name=domain_name)
        # Recieve packet
        result = DNS_Client.recieve()
    except ValidationError as e:
        print(str(e))

        sys.exit(0)

    # Check for errors
    if result['errors'] is not None:
        print(f"There was an error while handling a dns query.\n \
                Error message: {result['errors']}")
    else:
        print(f"Success!\n\nDomain name: {result['domain_name']}\nIP address: {result['ip_address']}")
