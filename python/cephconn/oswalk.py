import os

# 递归寻找路径下所有文件
PATH = "/home/matrix/go/src/github.com/Konmyn/language_basics/python"

for i in os.walk(PATH):
    current_path, _, files = i
    for f in files:
        file_path = os.path.join(current_path, f)
        print(file_path)
