# 返回字符串s包含字符串t的首坐标列表
def multi_find(s, t, trunc=0):
    if (not s) or (not t):
        return []
    result = list()
    loc = s.find(t)
    if loc == -1:
        return []
    else:
        result.append(loc+trunc)
        result.extend(multi_find(s[loc+len(t):], t, trunc=loc+len(t)+trunc))
    return result


if __name__ == "__main__":
    s1 = "hello world, world hello"
    t1 = ""
    r = multi_find(s1, t1)
    print(r)
