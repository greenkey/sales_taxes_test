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

    item = add_taxes({
        "quantity": 1,
        "description": "1 imported bottle of perfume",
        "price": Decimal("47.50"),
    })
    assert item["taxes"] == Decimal("7.15")
    assert item["total_price"] == Decimal("54.65")


def test_final_output():
    input_lines = [
        "1 book at 12.49",
        "1 music CD at 14.99",
        "1 chocolate bar at 0.85",
    ]
    output = produce_final_output(
        [i for i in get_items_from_file(input_lines)])
    assert output.split("\n") == [
        "1 book: 12.49",
        "1 music CD: 16.49",
        "1 chocolate bar: 0.85",
        "Sales Taxes: 1.50",
        "Total: 29.83",
    ]

    input_lines = [
        "1 imported box of chocolates at 10.00",
        "1 imported bottle of perfume at 47.50",
    ]
    output = produce_final_output(
        [i for i in get_items_from_file(input_lines)])
    assert output.split("\n") == [
        "1 imported box of chocolates: 10.50",
        "1 imported bottle of perfume: 54.65",
        "Sales Taxes: 7.65",
        "Total: 65.15",
    ]

    input_lines = [
        "1 imported bottle of perfume at 27.99",
        "1 bottle of perfume at 18.99",
        "1 packet of headache pills at 9.75",
        "1 box of imported chocolates at 11.25",
    ]
    output = produce_final_output(
        [i for i in get_items_from_file(input_lines)])
    assert output.split("\n") == [
        "1 imported bottle of perfume: 32.19",
        "1 bottle of perfume: 20.89",
        "1 packet of headache pills: 9.75",
        "1 imported box of chocolates: 11.85",
        "Sales Taxes: 6.70",
        "Total: 74.68",
    ]
