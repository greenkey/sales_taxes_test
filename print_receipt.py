import fileinput
import re
from decimal import Decimal
import math

from sales_taxes import get_rate


def main():
    items = [i for i in get_items_from_file(fileinput.input())]

    print(produce_final_output(items))


def get_items_from_file(file_handler):
    for line in file_handler:
        item = parse_input_line(line)

        item = add_taxes(item)

        yield item


def produce_final_output(items):
    output = []
    for item in items:
        output.append("{} {}: {:.2f}".format(
            item["quantity"],
            item["description"],
            item["price"] + item["taxes"],
        ))

    output.append("Sales Taxes: {:.2f}".format(
        sum([i["taxes"] for i in items])
    ))

    output.append("Total: {:.2f}".format(
        sum([i["total_price"] for i in items])
    ))

    return "\n".join(output)


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
    rate = get_rate(item["description"])
    raw_tax = item["price"] * rate * item["quantity"]
    item["taxes"] = math.ceil(raw_tax / Decimal("0.05")) * Decimal("0.05")
    item["total_price"] = item["taxes"] + item["price"] * item["quantity"]
    return item


if __name__ == "__main__":
    main()
