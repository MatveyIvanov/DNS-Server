import bitstring
import codecs
from dataclasses import asdict
from typing import Tuple, List, Union

from config import config
from dnsclient.abstract import UDPPacket, UDPHandler
from utils.entities import DNSQueryBase, DNSResponse, DNSQuery, DNSFormat


class DNSPacket(UDPPacket[str]):
    content: str

    def __call__(self, content: str) -> bytes:
        """
        Build UDP packet with domain name for DNS query
        """
        self._format_content(content)
        query, format = self._build_dns_query(self.content)
        return bitstring.pack(",".join(format), **query).tobytes()

    def _format_content(self, content: str) -> None:
        self.content = content.split(".")

    def _base_dns_query(self) -> DNSQueryBase:
        return DNSQueryBase(
            id="0x1a2b",
            flags="0b0000000100000000",  # Standard query. RD=1: ask only for IP
            qdcount=1,  # One question
            ancount=0,
            nscount=0,
            arcount=0,
        )

    def _base_dns_format(self) -> List[str]:
        # Construct the DNS packet consisting of header + QNAME + QTYPE + QCLASS.
        return [
            "hex=id",
            "bin=flags",
            "uintbe:16=qdcount",
            "uintbe:16=ancount",
            "uintbe:16=nscount",
            "uintbe:16=arcount",
        ]

    def _build_dns_query(self, content: List[str]) -> Tuple[DNSQuery, DNSFormat]:
        # Add QNAME
        # <size><label><size><label>...<size><label>0x00
        query = asdict(self._base_dns_query())
        format = self._base_dns_format()

        j = 0
        for i, _ in enumerate(content):
            content[i] = content[i].strip()

            format.append("hex=qname" + str(j))
            query["qname" + str(j)] = self._to_hex_string(len(content[i]))

            j += 1

            format.append("hex=qname" + str(j))
            query["qname" + str(j)] = self._to_hex_string(content[i])

            j += 1

        # Add a terminating byte.
        format.append("hex=qname" + str(j))
        query["qname" + str(j)] = self._to_hex_string(0)

        # Add QTYPE
        format.append("uintbe:16=qtype")
        query["qtype"] = 1  # For the A record

        # Add QCLASS
        format.append("hex=qclass")
        query["qclass"] = "0x0001"  # For IN or Internet

        return query, format

    def _to_hex_string(self, value: Union[str, int]) -> str:
        """
        Encodes either a positive integer or string to its hexadecimal representation.
        """

        result = "0"

        if value.__class__.__name__ == "int" and value >= 0:
            result = hex(value)

            if value < 16:
                result = "0" + result[2:]

        elif value.__class__.__name__ == "str":
            result = "".join([hex(ord(symbol))[2:] for symbol in value])

        return "0x" + result


class DNSHandler(UDPHandler[DNSPacket, DNSResponse]):
    def __call__(self, content: bytes, packet: DNSPacket) -> DNSResponse:
        # Convert data to bit string.
        data = bitstring.BitArray(bytes=content)

        # Unpack the received UDP packet and extract the IP the host name resolved to.
        # Get the host name from the QNAME located just past the received header.

        host_name_from = []
        # First size of the NAME starts at bit 96 and goes up to bit 104.
        # <size><label><size><label>...<size><label>0x00

        x = 96
        y = x + 8

        for _, _ in enumerate(packet.content):
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
            host_name_from.append(codecs.decode(data[x:y].hex, "hex_codec").decode())

            # Set up the next iteration to get the next label size.
            # Assuming here that any label size is no bigger than
            # one byte.
            x = y
            y = x + 8  # Eight bits to a byte.

        # Get the response code.
        # This is located in the received DNS packet header at
        # bit 28 ending at bit 32.
        response_code = int(str(data[28:32].hex))

        if response_code == 0:
            # Success
            return DNSResponse(
                code=0,
                domain_name=".".join(host_name_from),
                ip=".".join(  # IP address is usually stored in the last four octets of the DNS packet for A records.
                    [
                        str(data[-32:-24].uintbe),
                        str(data[-24:-16].uintbe),
                        str(data[-16:-8].uintbe),
                        str(data[-8:].uintbe),
                    ]
                ),
            )

        return DNSResponse(
            code=response_code,
            domain_name=".".join(host_name_from),
            error=config.DNS_RESPONSE_ERRORS.get(
                response_code, config.DNS_RESPONSE_DEFAULT_ERROR
            ),
        )
