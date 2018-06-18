import json
import re


def get_rate(product_description):
    rate = 10.0

    category = get_category(product_description)
    if category in ["book", "food", "medical"]:
        rate = 0.0

    if is_imported(product_description):
        rate += 5.0

    return rate


def get_category(product_description):
    product_description = product_description.lower().strip()

    product_description = product_description.replace("product", "").strip()

    category_patterns = get_category_patterns()

    for category, patterns in category_patterns.items():
        for pattern in patterns:
            print(pattern, product_description)
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
