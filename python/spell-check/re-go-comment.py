import re

# https://stackoverflow.com/questions/25822749/python-regex-for-matching-single-line-and-multi-line-comments
p = r"(?://[^\n]*|/\*(?:(?!\*/).)*\*/)"

with open("test.go", "r") as f:
    t = f.read()

m = re.findall(p, t, re.DOTALL)

print(m)
