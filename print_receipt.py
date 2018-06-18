import fileinput
import re
from decimal import Decimal
from sales_taxes import get_rate


def main():
    for line in fileinput.input():
        item = parse_input_line(line)

        item = add_taxes(item)

        print("{} {}: {}".format(
            item["quantity"],
            item["description"],
            item["price"] + item["taxes"],
        ))


def parse_input_line(line):
    m = re.match(r"^([0-9]+) +(.*) +at +([0-9\.]+)", line)

    if m is None:
        return None

    return {
        "quantity": int(m.group(1)),
        "description": m.group(2).strip(),
        "price": Decimal(m.group(3)),
    }


def add_taxes(item):
    item["taxes"] = item["price"] * \
        get_rate(item["description"]) * item["quantity"]
    item["total_price"] = item["taxes"] + item["price"] * item["quantity"]
    return item


if __name__ == "__main__":
    main()
