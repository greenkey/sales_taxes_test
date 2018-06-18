from sales_taxes import *

def test_get_rate():
    cases = [
        ("book", 0.0),
        ("food", 0.0),
        ("medical product", 0.0),
        ("perfume", 10.0),
        ("car", 10.0),
        ("laptop", 10.0),
    ]

    for product, expected_rate in cases:
        assert get_rate(product) == expected_rate