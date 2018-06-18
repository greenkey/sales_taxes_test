from decimal import Decimal

from print_receipt import *


def test_parse_input_line():
    p = parse_input_line("1 book at 12.49")
    assert p["quantity"] == 1
    assert p["description"] == "book"
    assert p["price"] == Decimal("12.49")

    p = parse_input_line("1 box of imported chocolates at 11.25")
    assert p["quantity"] == 1
    assert p["description"] == "box of imported chocolates"
    assert p["price"] == Decimal("11.25")
