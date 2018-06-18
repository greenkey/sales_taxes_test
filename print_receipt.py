import fileinput
import re
from decimal import Decimal


def main():
    for line in fileinput.input():
        print(line)


def parse_input_line(line):
    m = re.match(r"^([0-9]) (.*) at ([0-9\.]+)", line)
    return {
        "quantity": int(m.group(1)),
        "description": m.group(2),
        "price": Decimal(m.group(3)),
    }


if __name__ == "__main__":
    main()
