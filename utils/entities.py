import argparse
from dataclasses import dataclass
from typing import List, Any, Dict, Union, Tuple


@dataclass
class CLIArgument:
    flags: Tuple[str]
    help: str = ""
    default: Any = None
    const: Any = None
    nargs: str | None = None
    choices: List[str] | None = None
    action: argparse.Action | None = None


@dataclass
class DNSRecordQuery:
    domain_name: str
    many: bool
    force: bool


@dataclass
class DNSRecordResponse:
    domain_name: str
    many: bool
    ips: List[str] | None = None
    error: str | None = None


@dataclass
class DNSQueryBase:
    id: str
    flags: str
    qdcount: int
    ancount: int
    nscount: int
    arcount: int


@dataclass
class DNSResponse:
    code: int
    domain_name: str
    ip: str | None = None
    error: str | None = None


DNSQuery = Dict[str, Union[str, int]]
DNSFormat = List[str]
