import json
import re
import math
from decimal import Decimal


""" This module contains utilities to manipulate receipt items and to calculate
    taxes on them.
"""


def get_rate(product_description, imported=False):
    """ Returns the tax rate for a given product description.

    The calculation is based on the category of the product.
    For other information on tax calculation, see main documentation.

    Args:
        product_description (str): The description of the product.
        imported (bool): default=False; Is the product an imported one?

    Returns:
        Decimal: the tax rate. Using Decimal for maximum precision.

    """

    rate = Decimal(".10")

    category = get_category(product_description)
    if category in ["book", "food", "medical"]:
        rate = Decimal("0")

    if imported:
        rate = rate + Decimal(".05")

    return rate


def get_category(product_description):
    """ Retrieve the category based on the product description.

    Every category has a set of regexp patterns (see `get_category_patterns`)
    used to match the product description.

    Args:
        product_description (str): The description of the product.

    Returns:
        str: The category.

    """

    product_description = product_description.replace("product", "").strip()

    category_patterns = get_category_patterns()

    for category, patterns in category_patterns.items():
        for pattern in patterns:
            if re.match(pattern, product_description):
                return category

    return product_description


def get_category_patterns():
    """ Retrieve all the patterns to match the products into categories.

    WARNING: currently the function has an hard-coded filename:
    `product_category_patterns.json`.

    Returns:
        dict: The list of regexp patterns for every product category.

    """

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
        return self.price * self.quantity + self.total_tax

    @property
    def total_tax(self):
        raw_tax = self.tax_rate * self.price * self.quantity
        # rounding up to the nearest 0.05
        return math.ceil(raw_tax / Decimal("0.05")) * Decimal("0.05")

    @property
    def imported(self):
        return "imported" in self.full_description

    def __str__(self):
        """The string representation of the object, for output purposes
        """

        imported_string = "imported " if self.imported else ""

        return f"{self.quantity} {imported_string}{self.clean_description}: {self.total_price:.2f}"
