

def get_rate(product_description):
    category = get_category(product_description)
    if category in ["book", "food", "medical"]:
        return 0.0
    return 10.0


def get_category(product_description):
    product_description = product_description.lower().strip()

    product_description = product_description.replace("product", "").strip()

    if "chocolate" in product_description:
        return "food"

    return product_description