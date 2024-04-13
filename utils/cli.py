import sys
import os
from argparse import ArgumentParser
from typing import Tuple, List

from config import config
from dnsclient.abstract import CLI
from dnsclient.query import Query
from utils.entities import CLIArgument, DNSRecordQuery, DNSRecordResponse


class color:
    PURPLE = "\033[95m"
    CYAN = "\033[96m"
    DARKCYAN = "\033[36m"
    BLUE = "\033[94m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    RED = "\033[91m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"
    END = "\033[0m"


class DNSClientCLI(CLI):
    def __init__(
        self,
        parser: ArgumentParser,
        arguments: Tuple[CLIArgument],
        query: Query,
        owidth: int | None = None,  # output width
    ):
        self.parser = parser
        self.arguments = arguments
        self.query = query
        self.owidth = owidth

        self._init_arguments()

    def _init_arguments(self) -> None:
        for argument in self.arguments:
            kwargs = {
                "help": argument.help,
                "default": argument.default,
                "const": argument.const,
                "nargs": argument.nargs,
                "choices": argument.choices,
                "action": argument.action,
            }
            self.parser.add_argument(
                *argument.flags, **{k: v for k, v in kwargs.items() if v is not None}
            )

    def run(self, args: List[str]) -> None:
        self._validate_args(args)
        namespace = self.parser.parse_args(args)
        result: DNSRecordResponse = self.query(  # type: ignore
            entry=DNSRecordQuery(
                domain_name=namespace.domain,
                many=namespace.many,
                force=namespace.force,
            )
        )

        if result.error:
            return self._show_error(result.error)
        return self._show_result(result)

    def _validate_args(self, args: List[str]) -> None:
        if len(args) == 0:
            self.parser.print_help()
            sys.exit(0)

    def _show_error(self, error: str) -> None:
        self._show(
            "There was an error while handling a dns query.",
            f'Error message: "{error}"',
            is_error=True,
        )

    def _show_result(self, result: DNSRecordResponse) -> None:
        ip_text = "IP address: "
        if len(result.ips) > 1:
            ip_text = "IP addresses: "

        ip = f"{result.ips.pop()}"

        self._show(
            "Success!",
            f"Domain name: {result.domain_name}",
            f"{ip_text}{ip}",
            *[" " * len(ip_text) + ip for ip in result.ips] if result.ips else "",
        )

    def _show(self, *texts: str, is_error: bool = False) -> None:
        width = self.owidth or (self._get_terminal_witdh() // 2)
        print(color.BOLD, color.RED if is_error else color.DARKCYAN)
        print("-" * width)
        print(*[text.center(width) for text in texts], sep="\n")
        print("-" * width)
        print(color.GREEN, config.CLI_GRATITUDE)
        print(color.END)

    def _get_terminal_witdh(self) -> int:
        return os.get_terminal_size().columns
