import sys
from typing import List

from config.di import Container


def main(args: List[str]):
    container = Container()
    container.cli().run(args)


if __name__ == "__main__":
    main(sys.argv[1:])
