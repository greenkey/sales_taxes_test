from sales_taxes import *


def test_get_rate():
    cases = [
        ("book", 0.0),
        ("food", 0.0),
        ("medical product", 0.0),
        ("perfume", 10.0),
        ("car", 10.0),
        ("laptop", 10.0),
        ("music CD", 10.0),
        ("chocolate bar", 0.0),
        ("box of chocolates", 0.0),
        ("bottle of perfume", 10.0),
        ("headache pills", 0.0),
        ("chocolates", 0.0),
    ]

    for product, expected_rate in cases:
        assert get_rate(product) == expected_rate


def test_get_product_category():
    cases = [
        ("chocolate bar", "food"),
        ("unknown product", "unknown"),
        ("chocolate face cream", "self-care"),
        ("headache pills", "medical"),
        ("stomachache cream", "medical"),
    ]

    # TODO: mock get_category_patterns

    for prod_description, category_expected in cases:
        assert get_category(prod_description) == category_expected


def test_recognise_imported_product():
    cases = [
        ("book", False),
        ("music CD", False),
        ("chocolate bar", False),
        ("imported box of chocolates", True),
        ("imported bottle of perfume", True),
        ("imported bottle of perfume", True),
        ("bottle of perfume", False),
        ("packet of headache pills", False),
        ("box of imported chocolates", True),
    ]

    for product_description, expected_imported_flag in cases:
        assert is_imported(product_description) == expected_imported_flag
