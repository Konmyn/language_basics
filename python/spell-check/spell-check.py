import os
import re

from spellchecker import SpellChecker

spell = SpellChecker()
ext_cache = set()
uncache = set()

regex = r'\b\w+\b'
pt_url = r"""(?i)\b((?:https?:(?:/{1,3}|[a-z0-9%])|[a-z0-9.\-]+[.](?:com|net|org|edu|gov|mil|aero|asia|biz|cat|coop|info|int|jobs|mobi|museum|name|post|pro|tel|travel|xxx|ac|ad|ae|af|ag|ai|al|am|an|ao|aq|ar|as|at|au|aw|ax|az|ba|bb|bd|be|bf|bg|bh|bi|bj|bm|bn|bo|br|bs|bt|bv|bw|by|bz|ca|cc|cd|cf|cg|ch|ci|ck|cl|cm|cn|co|cr|cs|cu|cv|cx|cy|cz|dd|de|dj|dk|dm|do|dz|ec|ee|eg|eh|er|es|et|eu|fi|fj|fk|fm|fo|fr|ga|gb|gd|ge|gf|gg|gh|gi|gl|gm|gn|gp|gq|gr|gs|gt|gu|gw|gy|hk|hm|hn|hr|ht|hu|id|ie|il|im|in|io|iq|ir|is|it|je|jm|jo|jp|ke|kg|kh|ki|km|kn|kp|kr|kw|ky|kz|la|lb|lc|li|lk|lr|ls|lt|lu|lv|ly|ma|mc|md|me|mg|mh|mk|ml|mm|mn|mo|mp|mq|mr|ms|mt|mu|mv|mw|mx|my|mz|na|nc|ne|nf|ng|ni|nl|no|np|nr|nu|nz|om|pa|pe|pf|pg|ph|pk|pl|pm|pn|pr|ps|pt|pw|py|qa|re|ro|rs|ru|rw|sa|sb|sc|sd|se|sg|sh|si|sj|Ja|sk|sl|sm|sn|so|sr|ss|st|su|sv|sx|sy|sz|tc|td|tf|tg|th|tj|tk|tl|tm|tn|to|tp|tr|tt|tv|tw|tz|ua|ug|uk|us|uy|uz|va|vc|ve|vg|vi|vn|vu|wf|ws|ye|yt|yu|za|zm|zw)/)(?:[^\s()<>{}\[\]]+|\([^\s()]*?\([^\s()]+\)[^\s()]*?\)|\([^\s]+?\))+(?:\([^\s()]*?\([^\s()]+\)[^\s()]*?\)|\([^\s]+?\)|[^\s`!()\[\]{};:'".,<>?«»“”‘’])|(?:(?<!@)[a-z0-9]+(?:[.\-][a-z0-9]+)*[.](?:com|net|org|edu|gov|mil|aero|asia|biz|cat|coop|info|int|jobs|mobi|museum|name|post|pro|tel|travel|xxx|ac|ad|ae|af|ag|ai|al|am|an|ao|aq|ar|as|at|au|aw|ax|az|ba|bb|bd|be|bf|bg|bh|bi|bj|bm|bn|bo|br|bs|bt|bv|bw|by|bz|ca|cc|cd|cf|cg|ch|ci|ck|cl|cm|cn|co|cr|cs|cu|cv|cx|cy|cz|dd|de|dj|dk|dm|do|dz|ec|ee|eg|eh|er|es|et|eu|fi|fj|fk|fm|fo|fr|ga|gb|gd|ge|gf|gg|gh|gi|gl|gm|gn|gp|gq|gr|gs|gt|gu|gw|gy|hk|hm|hn|hr|ht|hu|id|ie|il|im|in|io|iq|ir|is|it|je|jm|jo|jp|ke|kg|kh|ki|km|kn|kp|kr|kw|ky|kz|la|lb|lc|li|lk|lr|ls|lt|lu|lv|ly|ma|mc|md|me|mg|mh|mk|ml|mm|mn|mo|mp|mq|mr|ms|mt|mu|mv|mw|mx|my|mz|na|nc|ne|nf|ng|ni|nl|no|np|nr|nu|nz|om|pa|pe|pf|pg|ph|pk|pl|pm|pn|pr|ps|pt|pw|py|qa|re|ro|rs|ru|rw|sa|sb|sc|sd|se|sg|sh|si|sj|Ja|sk|sl|sm|sn|so|sr|ss|st|su|sv|sx|sy|sz|tc|td|tf|tg|th|tj|tk|tl|tm|tn|to|tp|tr|tt|tv|tw|tz|ua|ug|uk|us|uy|uz|va|vc|ve|vg|vi|vn|vu|wf|ws|ye|yt|yu|za|zm|zw)\b/?(?!@)))"""
pt_note = r"@\w+"
pt_num = r"#\w+"
pt_comment = r"(?://[^\n]*|/\*(?:(?!\*/).)*\*/)"
pt_print = r'\("(.*?)"'

# TODO(madhusudancs)
# @mindprince
# "github.com/mindprince/gonvml"

w = list()
with open("words.txt") as f:
    for line in f.readlines():
        if line.startswith("#"):
            continue
        w.extend(line.strip().split())
# 载入非错误单词（手工认证）
spell.word_frequency.load_words(w)


def main(code_path=None):
    if not code_path:
        return
    for dir, _, fnames in os.walk(code_path):
        for f in fnames:
            fpath = os.path.join(dir, f)
            # print(fpath)
            feed(fpath)


def feed(fpath=None):
    if not fpath:
        return
    # 先跳过包管理目录
    if "/vendor/" in fpath:
        return
    ext = os.path.splitext(fpath)[-1]
    # 对markdown格式的文件进行检索
    # if ext == ".md":
    #     # print(fpath)
    #     read_md(fpath)
    if ext == ".go":
        read_go(fpath)


# 扫描markdown文件
def read_md(file):
    global uncache
    with open(file, "r") as f:
        linenum = 0
        for l in f.readlines():
            origins = l
            linenum += 1
            # 删除url
            l = re.sub(pt_url, "", l)
            # 删除@someone这种格式的人名
            l = re.sub(pt_note, "", l)
            # 删除#someone这种格式的人名
            l = re.sub(pt_num, "", l)
            # 进行第一次分词
            words = re.findall(regex, l)
            nwords = list()
            for w in words:
                # 跳过带连字符或者包含数字的词
                if "_" in w or re.match(r".*\d.*", w):
                    continue
                # 对camelcase的词进行二次分词
                nw = re.findall(r'[A-Z]?[a-z]+|[A-Z]+(?=[A-Z]|$)', w)
                nwords.extend(nw)
            unkn = spell.unknown(nwords)
            if not unkn:
                continue
            # print(file, '@', linenum, '->', *unkn)
            # print(origins)
            uncache = uncache.union(unkn)


# 扫描go文件
def read_go(file):
    for i in [
        "kubectl/explain/formatter_test.go",
        "kubectl/explain/model_printer_test.go",
        "kubectl/explain/fields_printer_test.go",
        "/generated/",
    ]:
        if i in file:
            return
    global uncache
    with open(file, "r") as f:
        t = f.read()
    # comments = re.findall(pt_comment, t, re.DOTALL)
    comments = re.findall(pt_print, t, re.DOTALL)
    comments = " ".join(comments)
    # 删除url
    comments = re.sub(pt_url, "", comments)
    # 删除@someone这种格式的人名
    comments = re.sub(pt_note, "", comments)
    # 删除#someone这种格式的人名
    comments = re.sub(pt_num, "", comments)
    words = re.findall(regex, comments)
    nwords = list()
    for w in words:
        # 跳过带连字符或者包含数字的词
        if "_" in w or re.match(r".*\d.*", w):
            continue
        # 对camelcase的词进行二次分词
        nw = re.findall(r'[A-Z]?[a-z]+|[A-Z]+(?=[A-Z]|$)', w)
        nwords.extend(nw)
    unkn = spell.unknown(nwords)
    if not unkn:
        return
    print(file, unkn)
    uncache = uncache.union(unkn)
    comment_cache(file, unkn)


ccache = dict()


def comment_cache(file, nwords):
    global ccache
    l = len(nwords)
    if l not in ccache:
        ccache[l] = [1, [file]]
    else:
        ccache[l][0] += 1
        ccache[l][1].append(file)


def print_ccache():
    global ccache
    l = list(ccache.keys())
    l.sort()
    for i in reversed(l):
        print(i)
        print(ccache[i])


if __name__ == "__main__":
    # code_path = "/home/matrix/workspace/github/helm"
    code_path = "/home/matrix/go/src/k8s.io/kubernetes"
    # code_path = "/home/matrix/go/src/github.com/prometheus/prometheus"
    # code_path = "/home/matrix/workspace/github/envoy"
    # code_path = "/home/matrix/workspace/github/fluentd"
    # code_path = "/home/matrix/workspace/github/coredns"
    # code_path = "/home/matrix/workspace/github/containerd"
    # code_path = "/home/matrix/workspace/github/tikv"
    # code_path = "/home/matrix/workspace/github/etcd"
    main(code_path)
    # 把找到的所有错误单词存入临时文件
    result = list(uncache)
    result.sort()
    with open("tmp.txt", "w") as t:
        l = list()
        for i in result:
            l.append(i)
            if len(" ".join(l)) >= 80:
                t.write(" ".join(l) + "\n")
                l = list()
                continue
        else:
            t.write(" ".join(l) + "\n")
    print_ccache()
