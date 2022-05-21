from dns_client.Client import Client
from dns_client.exceptions import ValidationError


MAX_QUERIES_TO_GET_NEW_IP = 15
MAX_QUERIES = 100
MANY_FLAGS = ('-a', '--all') # If set then check for more than 1 IP

def process_dns_query(domain_name: str, many: bool) -> dict:
    result = {
        'domain_name': None,
        'ip_addresses': set(),
        'errors': None
    }

    DNS_Client = Client()
    repeat_count = 0
    total_repeat_count = 0
    while True:
        try:
            # Check for queries limit
            total_repeat_count += 1
            if total_repeat_count > MAX_QUERIES:
                break

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
            result['errors'] = str(e)
            break

    return result