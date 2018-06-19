import fileinput
import re
from decimal import Decimal
import math

from sales_taxes import get_rate, Item


def main():
    items = [i for i in get_items_from_file(fileinput.input())]

    print(produce_final_output(items))


def get_items_from_file(file_handler):
    for line in file_handler:
        item = Item()
        item.parse_description(line)
        yield item


def produce_final_output(items):
    output = []

    for item in items:
        output.append(str(item))

    output.append("Sales Taxes: {}".format(
        sum([i.total_tax for i in items])
    ))

    output.append("Total: {}".format(
        sum([i.total_price for i in items])
    ))

    return "\n".join(output)


if __name__ == "__main__":
    main()
