from typing import Tuple
from pathlib import Path

from dnsclient.abstract import Query, Client
from config import config
from utils.entities import DNSRecordQuery, DNSRecordResponse, DNSResponse


class QueryForLocalRecords(Query[DNSRecordQuery, DNSRecordResponse]):
    def __call__(self, entry: DNSRecordQuery) -> DNSRecordResponse | None:
        folder = self._mkdir()
        file, created = self._touch(folder)
        if created:
            self._fill_file(file)
        return self._find(file, entry)

    def _mkdir(self) -> Path:
        folder = Path(config.LOCAL_DNS_DIR / config.LOCAL_DNS_FOLDER)
        folder.mkdir(parents=True, exist_ok=True)
        return folder

    def _touch(self, folder: Path) -> Tuple[Path, bool]:
        file = Path(folder / config.LOCAL_DNS_FILE)
        created = False
        if not file.is_file():
            created = True
            file.touch()
        return file, created

    def _fill_file(self, file: Path) -> None:
        with file.open("w") as f:
            f.write(config.LOCAL_DNS_DESCRIPTION)
            for key, value in config.LOCAL_DNS_DEFAULT_RECORDS.items():
                f.write(f"{key} {value}\n")

    def _find(self, file: Path, entry: DNSRecordQuery) -> DNSRecordResponse | None:
        result = DNSRecordResponse(
            domain_name=entry.domain_name,
            many=entry.many,
            ips=[],
        )
        with file.open("r") as f:
            data = f.readlines()
            for line in data:
                line = line.strip(" ")
                if line.startswith(config.LOCAL_DNS_COMMENT_SYMBOL):
                    continue
                try:
                    domain, address = line.split(config.LOCAL_DNS_SPLIT_SYMBOL)
                except ValueError:  # Expecting `too many values to unpack`
                    continue
                if domain == entry.domain_name:
                    result.ips.append(address)
        if not result.ips:
            return None
        return result


class QueryForDNSRecords(Query[DNSRecordQuery, DNSRecordResponse]):
    def __init__(
        self,
        client: Client,
        query_local_records: Query,
        max_retries: int,
        max_retries_to_get_new_ip: int,
        max_queries: int,
    ) -> None:
        self.client = client
        self.query_local_records = query_local_records
        self.max_retries = max_retries
        self.max_retries_to_get_new_ip = max_retries_to_get_new_ip
        self.max_queries = max_queries

    def __call__(self, entry: DNSRecordQuery) -> DNSRecordResponse | None:
        response = self._query_local_records(entry)
        if response is not None:
            return response
        return self._query_dns_server(entry)

    def _query_local_records(self, entry: DNSRecordQuery) -> DNSRecordResponse | None:
        if entry.force:
            return None
        local_response = self.query_local_records(entry)
        if local_response:
            return DNSRecordResponse(
                domain_name=entry.domain_name,
                many=entry.many,
                ips=local_response,
            )
        return None

    def _query_dns_server(self, entry: DNSRecordQuery) -> DNSRecordResponse:
        result = DNSRecordResponse(
            domain_name=entry.domain_name, many=entry.many, ips=[]
        )
        same_ip_count, retries_count, queries_count = 0, 0, 0
        while queries_count <= self.max_queries:
            queries_count += 1

            packet = self.client.send(entry.domain_name)
            data: DNSResponse = self.client.recieve(packet)

            # retry on error block
            if data.error or data.ip is None:
                if retries_count >= self.max_retries:
                    result.ips.clear()
                    result.error = data.error
                    return result
                retries_count += 1
                continue
            retries_count = 0

            # retry on same IP block
            if entry.many and data.ip in result.ips:
                if same_ip_count >= self.max_retries_to_get_new_ip:
                    break
                same_ip_count += 1
                continue
            same_ip_count = 0

            result.ips.append(data.ip)
            if not entry.many:
                return result

        return result
