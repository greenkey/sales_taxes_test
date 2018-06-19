import json
import re
from decimal import Decimal


def get_rate(product_description):
    rate = Decimal(".10")

    category = get_category(product_description)
    if category in ["book", "food", "medical"]:
        rate = Decimal("0")

    if is_imported(product_description):
        rate = rate + Decimal(".05")

    return rate


def get_category(product_description):
    product_description = product_description.replace("product", "").strip()

    category_patterns = get_category_patterns()

    for category, patterns in category_patterns.items():
        for pattern in patterns:
            if re.match(pattern, product_description):
                return category

    return product_description


def get_category_patterns():
    # TODO: make the filename a setting
    filename = "product_category_patterns.json"

    try:
        return json.load(open(filename))

    except FileNotFoundError:
        print(
            f"Warning: Could not open file '{filename}', " +
            "cannot guess category from product name.")
        return {}

    except json.decoder.JSONDecodeError:
        raise Exception(f"The file '{filename}', " +
                        "is malformed, it should be a JSON.")


def is_imported(product_description):
    return "imported" in product_description


class Item():

    description_parser = r"^([0-9]+) +(.*) +at +([0-9\.]+)"

    def parse_description(self, description):
        """Read a string containing item information and tries to parse them.

        The string should be something like:
        `<no. of items> <item description> <cost of single item>`
        In the item description there could be the string "imported", this will
        set the imported flag in the object.

        Args:
            description (str): The string to be parsed.

        Returns:
            bool: True for success, False otherwise.

        """

        m = re.match(self.description_parser, description)

        if m is None:
            return False

        self.full_description = m.group(2).strip().lower()
        self.clean_description = self.full_description

        self.imported = is_imported(self.full_description)
        if self.imported:
            self.clean_description = self.full_description.replace(
                "imported", "").replace(
                "  ", " ").strip()

        self.quantity = int(m.group(1))
        self.price = Decimal(m.group(3))

        return True
