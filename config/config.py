import argparse
from pathlib import Path

from utils.entities import CLIArgument


CLI_GREETING = """
 _    _  ____  __    ___  _____  __  __  ____    ____  _____    ____  _  _  ____  _   _  _____  _  _
( \/\/ )( ___)(  )  / __)(  _  )(  \/  )( ___)  (_  _)(  _  )  (  _ \( \/ )(_  _)( )_( )(  _  )( \( )
 )    (  )__)  )(__( (__  )(_)(  )    (  )__)     )(   )(_)(    )___/ \  /   )(   ) _ (  )(_)(  )  (
(__/\__)(____)(____)\___)(_____)(_/\/\_)(____)   (__) (_____)  (__)   (__)  (__) (_) (_)(_____)(_)\_)
 ____  _  _  ___     ___  __    ____  ____  _  _  ____ /\\
(  _ \( \( )/ __)   / __)(  )  (_  _)( ___)( \( )(_  _))(
 )(_) ))  ( \__ \  ( (__  )(__  _)(_  )__)  )  (   )(  \/
(____/(_)\_)(___/   \___)(____)(____)(____)(_)\_) (__) ()\n
"""
CLI_GRATITUDE = """
 ____  _  _   __   __ _  __ _    _  _  __   _  _    ____  __  ____    _  _  ____  __  __ _   ___
(_  _)/ )( \ / _\ (  ( \(  / )  ( \/ )/  \ / )( \  (  __)/  \(  _ \  / )( \/ ___)(  )(  ( \ / __)
  )(  ) __ (/    \/    / )  (    )  /(  O )) \/ (   ) _)(  O ))   /  ) \/ (\___ \ )( /    /( (_ \\
 (__) \_)(_/\_/\_/\_)__)(__\_)  (__/  \__/ \____/  (__)  \__/(__\_)  \____/(____/(__)\_)__) \___/
 ____  _  _  ____  _  _   __   __ _    ____  __ _  ____     ___  __    __  ____  __ _  ____  _   
(  _ \( \/ )(_  _)/ )( \ /  \ (  ( \  (    \(  ( \/ ___)   / __)(  )  (  )(  __)(  ( \(_  _)/ \  
 ) __/ )  /   )(  ) __ ((  O )/    /   ) D (/    /\___ \  ( (__ / (_/\ )(  ) _) /    /  )(  \_/  
(__)  (__/   (__) \_)(_/ \__/ \_)__)  (____/\_)__)(____/   \___)\____/(__)(____)\_)__) (__) (_)
"""
CLI_DESCRIPTION = "DNS Client CLI"
CLI_ARGUMENTS = (
    CLIArgument(flags=("domain",), help="Domain name to check"),
    CLIArgument(
        flags=("-f", "--force"),
        help=(
            "If set, the program will skip local DNS records and make a request to DNS"
            " server."
        ),
        action=argparse.BooleanOptionalAction,
    ),
    CLIArgument(
        flags=("-m", "--many"),
        help="If set, the program will search for multiple IP adresses.",
        action=argparse.BooleanOptionalAction,
    ),
)
CLI_OWIDTH = 97  # output width

DNS_SERVER_IP = "8.8.8.8"
DNS_SERVER_PORT = 53
DNS_RESPONSE_ERRORS = {
    1: "Format error. Unable to interpret query.",
    2: "Server failure. Unable to process query.",
    3: "Name error. Domain name does not exist.",
    4: "Query request type not supported.",
    5: "Server refused query.",
    6: "Name that should not exist, does exist.",
    7: "RRset that should not exist, does exist.",
    8: "Server not authoritative for the zone.",
    9: "Name not in zone.",
}
DNS_RESPONSE_DEFAULT_ERROR = "Unknown response code. Try again later."

QUERY_MAX_RETRIES_TO_GET_NEW_IP = 5  # Maximum of queries to get new IP from DNS server
QUERY_MAX_RETRIES = 3  # Maximum of queries to get a valid response from DNS server
QUERY_MAX = 25  # Max queries limiter

LOCAL_DNS_DIR = Path.home()
LOCAL_DNS_FOLDER = ".local-dns"
LOCAL_DNS_FILE = ".local-dns-records"
LOCAL_DNS_DESCRIPTION = (
    "# Add your own DNS records. DNS record format: '<domain_name> <ip_address>'.\n#"
    " Note that there should be a newline right after <ip_address> and exactly 1 space"
    " between <domain_name> and <ip_address>.\n# The best practice would be to use"
    " below records as the examples for your own ones.\n# Lines starting with '#' will"
    " be ignored.\n"
)
LOCAL_DNS_DEFAULT_RECORDS = {"localhost": "127.0.0.1", "::1": "127.0.0.1"}
LOCAL_DNS_COMMENT_SYMBOL = "#"
LOCAL_DNS_SPLIT_SYMBOL = " "
