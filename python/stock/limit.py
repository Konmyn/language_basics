import argparse
from decimal import Decimal as D

parser = argparse.ArgumentParser()
parser.add_argument("-u", "--up", help="limit direction, up or down, default is down", action="store_true")
parser.add_argument("-d", "--day", help="days to continue", default=10, type=int)
parser.add_argument("-p", "--price", help="price to start", default="10")
args = parser.parse_args()

LIMIT_UP = "1.1"
LIMIT_DOWN = "0.9"
if args.up:
    rate, ratef = D(LIMIT_UP), float(LIMIT_UP)
else:
    rate, ratef = D(LIMIT_DOWN), float(LIMIT_DOWN)

price = D(args.price)
pricef = float(args.price)

previous_price, previous_pricef = None, None

table = "{:<4}: {:>8} {:>8}"

print(table.format("day", "decimal", "float"))

for i in range(1, args.day+1):
    price = round(price*rate, 2)
    pricef = round(pricef*ratef, 2)
    print(table.format(i, price, pricef))
    i += 1
    if previous_price == price and previous_pricef == pricef:
        print("price to low to go down, break")
        break
    previous_price, previous_pricef = price, pricef
