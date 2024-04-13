from pathlib import Path
from unittest import mock

from pytest_mock import MockerFixture

from config import config
from config.di import Container
from dnsclient.query import QueryForLocalRecords, QueryForDNSRecords
from utils.entities import DNSRecordQuery, DNSRecordResponse


class TestDNSPacket:
    pass


class TestDNSHandler:
    pass
