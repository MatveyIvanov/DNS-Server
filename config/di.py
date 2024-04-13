from argparse import ArgumentParser, RawDescriptionHelpFormatter

from dependency_injector import providers
from dependency_injector.containers import DeclarativeContainer

from config import config
from dnsclient.query import QueryForDNSRecords, QueryForLocalRecords
from dnsclient.client import DNSClient
from dnsclient.udp import DNSPacket, DNSHandler
from utils.cli import DNSClientCLI, color


class Container(DeclarativeContainer):
    parser = providers.Singleton(
        ArgumentParser,
        description=color.GREEN + config.CLI_GREETING + color.END,
        formatter_class=RawDescriptionHelpFormatter,
    )
    dns_packet = providers.Factory(DNSPacket)
    dns_handler = providers.Singleton(DNSHandler)
    dns_client = providers.Singleton(
        DNSClient,
        ip=config.DNS_SERVER_IP,
        port=config.DNS_SERVER_PORT,
        packet=dns_packet,
        handler=dns_handler,
    )
    query_local_records = providers.Singleton(QueryForLocalRecords)
    query_dns_records = providers.Singleton(
        QueryForDNSRecords,
        client=dns_client,
        query_local_records=query_local_records,
        max_retries=config.QUERY_MAX_RETRIES,
        max_retries_to_get_new_ip=config.QUERY_MAX_RETRIES_TO_GET_NEW_IP,
        max_queries=config.QUERY_MAX,
    )
    cli = providers.Singleton(
        DNSClientCLI,
        parser=parser,
        arguments=config.CLI_ARGUMENTS,
        query=query_dns_records,
        owidth=config.CLI_OWIDTH,
    )
