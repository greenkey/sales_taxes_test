# Sales Taxes

This is a command line utility to that prints out the receipt details for a shopping basket.

The receipt is the list of all the items and their price (including tax), finishing with the total cost of the items, and the total amounts of sales taxes paid.

## How to use

The program reads the input via the standard input, so you can use pipes and othe shell's input/ouput redirects:

    python3 print_receipt.py < input_file
    # or
    cat input_file | python3 print_receipt.py

### How taxes are calculated

Basic sales tax is applicable at a rate of 10% on all goods, except books, food, and medical products that are exempt. Import duty is an additional sales tax applicable on all imported goods at a rate of 5%, with no exemptions.

### Rounding rules

The rounding rules for sales tax are that for a tax rate of n%, a shelf price of p contains (np/100 rounded up to the nearest 0.05) amount of sales tax.

## Dev environment

Create your local environment with virtualenv, then install all the required packages:

    python3 -m venv .venv
    . .venv/bin/activate
    pip install -r dev_requirements.txt

To execute the tests use `pytest`.