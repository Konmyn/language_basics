from decimal import Decimal as D

day = 20

price = D("10")
rate = D("0.9")
for i in range(1, day+1):
    price = price*rate
    price = round(price, 2)
    print(i, ":", price)
    i += 1

pricef = 10
ratef = 0.9
for i in range(1, day+1):
    pricef = pricef*ratef
    pricef = round(pricef, 2)
    print(i, ":", pricef)
    i += 1
