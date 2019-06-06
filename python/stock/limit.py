import argparse
from decimal import Decimal as D

parser = argparse.ArgumentParser()
parser.add_argument("-u", "--up", help="limit direction, up or down, default is down", action="store_true")
parser.add_argument("-s", "--st", help="whether the stock is st or not", action="store_true")
parser.add_argument("-d", "--day", help="days to continue", default=10, type=int)
parser.add_argument("-p", "--price", help="price to start", default="10")
args = parser.parse_args()

if args.st:
    LIMIT_UP = "1.05"
    LIMIT_DOWN = "0.95"
else:
    LIMIT_UP = "1.1"
    LIMIT_DOWN = "0.9"

if args.up:
    rate, ratef = D(LIMIT_UP), float(LIMIT_UP)
else:
    rate, ratef = D(LIMIT_DOWN), float(LIMIT_DOWN)


def new_round(price):
    lprice = int(price * 1000)
    # print(lprice)
    if lprice % 10 >= 5:
        new_price = ((lprice // 10) + 1) / 100
    else:
        new_price = (lprice // 10) / 100
    # print(new_price)
    return round(new_price, 2)


price = D(args.price)
pricef = float(args.price)

previous_price, previous_pricef = None, None

table = "{:<4}: {:>8} {:>8}"

print(table.format("day", "decimal", "float"))

for i in range(1, args.day+1):
    price = price*rate
    price = round(price, 2)
    pricef = new_round(pricef*ratef)
    print(table.format(i, price, pricef))
    i += 1
    if previous_price == price and previous_pricef == pricef:
        print("price to low to go down, break")
        break
    previous_price, previous_pricef = price, pricef
