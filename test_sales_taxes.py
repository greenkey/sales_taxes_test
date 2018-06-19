from decimal import Decimal

from sales_taxes import *


def test_get_rate():
    cases = [
        ("book", Decimal(".0")),
        ("food", Decimal(".0")),
        ("medical product", Decimal(".0")),
        ("perfume", Decimal(".10")),
        ("car", Decimal(".10")),
        ("laptop", Decimal(".10")),
        ("music CD", Decimal(".10")),
        ("chocolate bar", Decimal(".0")),
        ("box of chocolates", Decimal(".0")),
        ("bottle of perfume", Decimal(".10")),
        ("headache pills", Decimal(".0")),
        ("chocolates", Decimal(".0")),
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
        ("bottle of perfume", False),
        ("packet of headache pills", False),
        ("box of imported chocolates", True),
    ]

    for product_description, expected_imported_flag in cases:
        assert is_imported(product_description) == expected_imported_flag


def test_additional_taxt_for_imported_prod():
    cases = [
        ("imported box of chocolates", Decimal(".05")),
        ("imported bottle of perfume", Decimal(".15")),
        ("box of imported chocolates", Decimal(".05")),
    ]

    for product, expected_rate in cases:
        assert get_rate(product) == expected_rate


def test_create_item_from_description():
    item = Item()

    desc = "1 book at 12.49"
    assert item.parse_description(desc) is True
    assert item.quantity == 1
    assert item.full_description == "book"
    assert item.price == Decimal("12.49")
    assert item.imported is False
    assert item.clean_description == item.full_description

    desc = "100 box of imported chocolates at 11.25"
    assert item.parse_description(desc) is True
    assert item.quantity == 100
    assert item.full_description == "box of imported chocolates"
    assert item.price == Decimal("11.25")
    assert item.imported is True
    assert item.clean_description == "box of chocolates"

    desc = "music CD at 14.99"
    assert item.parse_description(desc) is False
