import json
import re
from decimal import Decimal


def get_rate(product_description, imported=False):
    rate = Decimal(".10")

    category = get_category(product_description)
    if category in ["book", "food", "medical"]:
        rate = Decimal("0")

    if imported:
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


class Item():

    description_parser = r"^(([0-9]+) +)?([\w ]*)( +at +([0-9\.]+))?$"

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

        self.full_description = self.clean_description = ""
        self.tax_rate = 0
        self.quantity = 0
        self.price = 0

        m = re.match(self.description_parser, description)

        if m is None:
            return False

        success = True

        self.full_description = m.group(3).strip()
        self.clean_description = self.full_description

        if self.imported:
            self.clean_description = self.full_description.replace(
                "imported", "").replace(
                "  ", " ").strip()

        self.tax_rate = get_rate(self.full_description, self.imported)

        try:
            self.quantity = int(m.group(2))
        except TypeError:
            success = False

        try:
            self.price = Decimal(m.group(5))
        except TypeError:
            success = False

        return success

    @property
    def total_price(self):
        return (self.price * (1+self.tax_rate)) * self.quantity

    @property
    def imported(self):
        return "imported" in self.full_description

    def __str__(self):
        """The string representation of the object, for output purposes
        """

        imported_string = "imported " if self.imported else ""

        return f"{self.quantity} {imported_string}{self.clean_description}: {self.total_price:.2f}"
