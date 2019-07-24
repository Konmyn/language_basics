import re

p = r'"(.*?)"'

with open("test1.go", "r") as f:
    t = f.read()

m = re.findall(p, t, re.DOTALL)

print(m)
