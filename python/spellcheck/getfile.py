import os

proj_path = "/home/matrix/workspace/github/kubernetes"


def walk_through(ppath):
    ftype = set()
    all_content = os.walk(ppath)
    for a in all_content:
        path, dirs, files = a
        for f in files:
            a = f.split(".")[-1]
            if a not in ftype:
                ftype.add(a)
                print(a)
            # full_path = os.path.join(path, f)
            # print(full_path)

walk_through(proj_path)