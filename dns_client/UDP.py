import bitstring
import codecs
from typing import Dict
from dns_client.utils import to_hex_string
from dns_client.exceptions import ValidationError


class UDP:
    # Construct the DNS packet consisting of header + QNAME + QTYPE + QCLASS.
    DNS_QUERY_FORMAT = [
        'hex=id',
        'bin=flags',
        'uintbe:16=qdcount',
        'uintbe:16=ancount',
        'uintbe:16=nscount',
        'uintbe:16=arcount',
    ]

    DNS_QUERY = {
        'id': '0x1a2b',
        'flags': '0b0000000100000000',  # Standard query. RD=1: ask only for IP
        'qdcount': 1,  # One question.
        'ancount': 0,
        'nscount': 0,
        'arcount': 0,
    }

    def __init__(self, message) -> None:
        self.__message = message
        self.__validated_response = None

    @property
    def builded_request(self) -> bytes:
        return self.__build_request()

    @property
    def validated_response(self) -> Dict:
        if not self.__validated_response:
            raise ValidationError('Response query is not validated yet. To perform validation, use <udp_object>.validate(data=<data>)')
        return self.__validated_response

    def __build_request(self) -> bytes:
        """
        Build UDP packet with defined message for DNS query
        """
        self.__message = self.__message.split('.')

        self.__build_request_section()

        # Convert the struct to a bit string.
        return bitstring.pack(','.join(self.DNS_QUERY_FORMAT), **self.DNS_QUERY).tobytes()

    def __build_request_section(self) -> None:
        # Add QNAME
        # <size><label><size><label>...<size><label>0x00
        j = 0
        for i, _ in enumerate(self.__message):
            self.__message[i] = self.__message[i].strip()

            self.DNS_QUERY_FORMAT.append('hex=qname' + str(j))
            self.DNS_QUERY['qname' + str(j)] = to_hex_string(len(self.__message[i]))

            j += 1

            self.DNS_QUERY_FORMAT.append('hex=qname' + str(j))
            self.DNS_QUERY['qname' + str(j)] = to_hex_string(self.__message[i])

            j += 1

        # Add a terminating byte.
        self.DNS_QUERY_FORMAT.append('hex=qname' + str(j))
        self.DNS_QUERY['qname' + str(j)] = to_hex_string(0)

        # Add QTYPE
        self.DNS_QUERY_FORMAT.append('uintbe:16=qtype')
        self.DNS_QUERY['qtype'] = 1  # For the A record.

        # Add QCLASS
        self.DNS_QUERY_FORMAT.append('hex=qclass')
        self.DNS_QUERY['qclass'] = '0x0001'  # For IN or Internet.

    def validate(self, data: bytes) -> None:
        self.__validated_response = self.__handle_response_query(data=data)

    def __handle_response_query(self, data: bytes) -> dict:
        result = {
            'domain_name': None,
            'ip_address': None,
            'errors': None
        }

        # Convert data to bit string.
        data = bitstring.BitArray(bytes=data)

        # Unpack the received UDP packet and extract the IP the host name resolved to.
        # Get the host name from the QNAME located just past the received header.

        host_name_from = []
        # First size of the NAME starts at bit 96 and goes up to bit 104.
        # <size><label><size><label>...<size><label>0x00

        x = 96
        y = x + 8

        for _, _ in enumerate(self.__message):
            # Based on the size of the next label indicated by
            # the 1 octet/byte before the label, read that many
            # bits after the octet/byte until next
            # label size appears
            

            # Get the label size in hex. Convert to an integer and times it
            # by 8 to get the number of bits.

            increment = int(str(data[x:y].hex), 16) * 8
            x = y
            y = x + increment

            # Read in the label and convert it to ASCII
            host_name_from.append(codecs.decode(data[x:y].hex, 'hex_codec').decode())

            # Set up the next iteration to get the next label size.
            # Assuming here that any label size is no bigger than
            # one byte.
            x = y
            y = x + 8  # Eight bits to a byte.

        # Get the response code.
        # This is located in the received DNS packet header at
        # bit 28 ending at bit 32.
        response_code = str(data[28:32].hex)

        # Check for errors.
        if response_code == '0':
            # Success
            result['domain_name'] = '.'.join(host_name_from)

            # IP address is usually stored in the last four octets of the DNS packet for A records.
            result['ip_address'] = '.'.join(
                [
                    str(data[-32:-24].uintbe),
                    str(data[-24:-16].uintbe),
                    str(data[-16:-8].uintbe),
                    str(data[-8:].uintbe),
                ]
            )

        elif response_code == '1':
            # Format error
            result['errors'] = 'Format error. Unable to interpret query.'
        elif response_code == '2':
            # Server error
            result['errors'] ='Server failure. Unable to process query.'
        elif response_code == '3':
            # Domain name does not exist
            result['errors'] ='Name error. Domain name does not exist.'
        elif response_code == '4':
            # DNS query type is not supported
            result['errors'] = 'Query request type not supported.'
        elif response_code == '5':
            # Query is refused
            result['errors'] ='Server refused query.'

        return result