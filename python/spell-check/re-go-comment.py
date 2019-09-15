import re

# https://stackoverflow.com/questions/25822749/python-regex-for-matching-single-line-and-multi-line-comments
# p = r"(?://[^\n]*|/\*(?:(?!\*/).)*\*/)"
# with open("test.go", "r") as f:
#     t = f.read()
# m = re.findall(p, t)

string = "qqre\ntewtweTODO(mk2342wiek)dsfgsd"
pattern_note = r"TODO\(.*\)"
string = re.sub(pattern_note, "", string)

print(string)
