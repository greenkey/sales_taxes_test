from decimal import Decimal

from print_receipt import *


def test_parse_input_line():
    p = parse_input_line("1 book at 12.49")
    assert p["quantity"] == 1
    assert p["description"] == "book"
    assert p["price"] == Decimal("12.49")

    p = parse_input_line("100 box of imported chocolates at 11.25")
    assert p["quantity"] == 100
    assert p["description"] == "box of imported chocolates"
    assert p["price"] == Decimal("11.25")

    p = parse_input_line("music CD at 14.99")
    assert p == None


def test_add_taxes_to_item():
    item = add_taxes({
        "quantity": 1,
        "description": "chocolate",
        "price": Decimal("10"),
    })
    assert item["taxes"] == 0
    assert item["total_price"] == 10

    item = add_taxes({
        "quantity": 5,
        "description": "imported chocolate",
        "price": Decimal("10"),
    })
    assert item["taxes"] == Decimal(10 * 0.05 * 5)
    assert item["total_price"] == 50 + item["taxes"]

    item = add_taxes({
        "quantity": 10,
        "description": "imported bottle of perfume",
        "price": Decimal("100"),
    })
    assert item["taxes"] == Decimal(100 * 0.15 * 10)
    assert item["total_price"] == 1000 + item["taxes"]
