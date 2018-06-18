

def get_rate(product_description):
    if product_description in ["book", "food", "medical product"]:
        return 0.0
    return 10.0