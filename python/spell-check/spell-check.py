import os
import re
from collections import defaultdict

from spellchecker import SpellChecker

cache = dict()

pattern_word = r'\b\w+\b'
pattern_url = r"""(?i)\b((?:https?:(?:/{1,3}|[a-z0-9%])|[a-z0-9.\-]+[.](?:com|net|org|edu|gov|mil|aero|asia|biz|cat|coop|info|int|jobs|mobi|museum|name|post|pro|tel|travel|xxx|ac|ad|ae|af|ag|ai|al|am|an|ao|aq|ar|as|at|au|aw|ax|az|ba|bb|bd|be|bf|bg|bh|bi|bj|bm|bn|bo|br|bs|bt|bv|bw|by|bz|ca|cc|cd|cf|cg|ch|ci|ck|cl|cm|cn|co|cr|cs|cu|cv|cx|cy|cz|dd|de|dj|dk|dm|do|dz|ec|ee|eg|eh|er|es|et|eu|fi|fj|fk|fm|fo|fr|ga|gb|gd|ge|gf|gg|gh|gi|gl|gm|gn|gp|gq|gr|gs|gt|gu|gw|gy|hk|hm|hn|hr|ht|hu|id|ie|il|im|in|io|iq|ir|is|it|je|jm|jo|jp|ke|kg|kh|ki|km|kn|kp|kr|kw|ky|kz|la|lb|lc|li|lk|lr|ls|lt|lu|lv|ly|ma|mc|md|me|mg|mh|mk|ml|mm|mn|mo|mp|mq|mr|ms|mt|mu|mv|mw|mx|my|mz|na|nc|ne|nf|ng|ni|nl|no|np|nr|nu|nz|om|pa|pe|pf|pg|ph|pk|pl|pm|pn|pr|ps|pt|pw|py|qa|re|ro|rs|ru|rw|sa|sb|sc|sd|se|sg|sh|si|sj|Ja|sk|sl|sm|sn|so|sr|ss|st|su|sv|sx|sy|sz|tc|td|tf|tg|th|tj|tk|tl|tm|tn|to|tp|tr|tt|tv|tw|tz|ua|ug|uk|us|uy|uz|va|vc|ve|vg|vi|vn|vu|wf|ws|ye|yt|yu|za|zm|zw)/)(?:[^\s()<>{}\[\]]+|\([^\s()]*?\([^\s()]+\)[^\s()]*?\)|\([^\s]+?\))+(?:\([^\s()]*?\([^\s()]+\)[^\s()]*?\)|\([^\s]+?\)|[^\s`!()\[\]{};:'".,<>?«»“”‘’])|(?:(?<!@)[a-z0-9]+(?:[.\-][a-z0-9]+)*[.](?:com|net|org|edu|gov|mil|aero|asia|biz|cat|coop|info|int|jobs|mobi|museum|name|post|pro|tel|travel|xxx|ac|ad|ae|af|ag|ai|al|am|an|ao|aq|ar|as|at|au|aw|ax|az|ba|bb|bd|be|bf|bg|bh|bi|bj|bm|bn|bo|br|bs|bt|bv|bw|by|bz|ca|cc|cd|cf|cg|ch|ci|ck|cl|cm|cn|co|cr|cs|cu|cv|cx|cy|cz|dd|de|dj|dk|dm|do|dz|ec|ee|eg|eh|er|es|et|eu|fi|fj|fk|fm|fo|fr|ga|gb|gd|ge|gf|gg|gh|gi|gl|gm|gn|gp|gq|gr|gs|gt|gu|gw|gy|hk|hm|hn|hr|ht|hu|id|ie|il|im|in|io|iq|ir|is|it|je|jm|jo|jp|ke|kg|kh|ki|km|kn|kp|kr|kw|ky|kz|la|lb|lc|li|lk|lr|ls|lt|lu|lv|ly|ma|mc|md|me|mg|mh|mk|ml|mm|mn|mo|mp|mq|mr|ms|mt|mu|mv|mw|mx|my|mz|na|nc|ne|nf|ng|ni|nl|no|np|nr|nu|nz|om|pa|pe|pf|pg|ph|pk|pl|pm|pn|pr|ps|pt|pw|py|qa|re|ro|rs|ru|rw|sa|sb|sc|sd|se|sg|sh|si|sj|Ja|sk|sl|sm|sn|so|sr|ss|st|su|sv|sx|sy|sz|tc|td|tf|tg|th|tj|tk|tl|tm|tn|to|tp|tr|tt|tv|tw|tz|ua|ug|uk|us|uy|uz|va|vc|ve|vg|vi|vn|vu|wf|ws|ye|yt|yu|za|zm|zw)\b/?(?!@)))"""
pattern_note = r"@\w+"  # @yourname
pattern_num = r"#\w+"   # #yourname
pattern_comment = r"(?://[^\n]*|/\*(?:(?!\*/).)*\*/)"  # /* comment */ or // comment
pattern_logging = r'\("(.*?)"'  # ("hello world"
pattern_camelcase = r'[A-Z]?[a-z]+|[A-Z]+(?=[A-Z]|$)'  # helloWorld


TYPO_WORDS_FILE = "tmp.txt"
KNOWN_WORDS_FILE = "words.txt"


def init_spell_check():
    checker = SpellChecker()
    w = list()
    with open(KNOWN_WORDS_FILE) as f:
        for line in f.readlines():
            if line.startswith("#"):
                continue
            w.extend(line.strip().split())
    # 载入非错误单词（手工认证）
    checker.word_frequency.load_words(w)
    return checker


spell = init_spell_check()


def run_spell_check(project=None, ext=(".go", ".md")):
    if not project:
        return
    for file in walk_dir(project):
        if get_file_extension(file) in ext:
            feed(file)


def run_file_ext_statistics(project=None):
    if not project:
        return
    statistics = defaultdict(int)
    for file in walk_dir(project):
        if not is_qualified_file(file):
            continue
        ext = get_file_extension(file)
        statistics[ext] += 1
    stat = [(k, v) for k, v in statistics.items()]
    stat = sorted(stat, key=lambda i: i[1], reverse=True)
    for i in stat:
        print("{:>20s}: {:<4d}".format(i[0], i[1]))


def walk_dir(project):
    for dir, _, fnames in os.walk(project):
        for f in fnames:
            file = os.path.join(dir, f)
            yield file


def is_qualified_file(file):
    if not file:
        return False
    # go项目，跳过go的包管理目录
    if "/vendor/" in file:
        return False
    # 跳过 .git 目录
    if "/.git/" in file:
        return False
    # kubernetes项目
    for i in [
        "kubectl/explain/formatter_test.go",
        "kubectl/explain/model_printer_test.go",
        "kubectl/explain/fields_printer_test.go",
        "/generated/",
    ]:
        if i in file:
            return False
    return True


def get_file_extension(file):
    return os.path.splitext(file)[-1]


def feed(file=None):
    if not is_qualified_file(file):
        return
    parse_misspelled(file)


def get_text(file):
    with open(file, "r") as f:
        text = f.read()
    if get_file_extension(file) == ".go":
        comments = re.findall(pattern_comment, text, re.DOTALL)
        logs = re.findall(pattern_logging, text, re.DOTALL)
        text = " ".join(comments) + " " + " ".join(logs)
    return text


def parse_words(string):
    string = string.replace('\n', ' ').replace('\r', '')
    # 删除url
    string = re.sub(pattern_url, "", string)
    # 删除@someone这种格式的人名
    string = re.sub(pattern_note, "", string)
    # 删除#someone这种格式的人名
    string = re.sub(pattern_num, "", string)
    # 进行第一次分词
    raw_words = re.findall(pattern_word, string)
    words = list()
    for w in raw_words:
        # 跳过带连字符或者包含数字的词
        if "_" in w or re.match(r".*\d.*", w):
            continue
        if len(w) <= 2:
            continue
        # 对camelcase的词进行二次分词
        word_list = re.findall(pattern_camelcase, w)
        words.extend(word_list)
    return words


def parse_misspelled(file):
    raw_text = get_text(file)
    words = parse_words(raw_text)
    bad_words = spell.unknown(words)
    if not bad_words:
        return
    update_cache(file, bad_words)


def update_cache(file, bad_words):
    global cache
    cache[file[27:]] = bad_words


def print_cache():
    global cache
    output = defaultdict(list)
    for k, v in cache.items():
        output[len(v)].append((k, v))
    lens = sorted(list(output.keys()), reverse=True)
    for i in lens:
        print("#", i)
        for j in output[i]:
            print(j[0], "->", j[1])


def save_typo_words():
    global cache
    bad_words = set()
    for v in cache.values():
        bad_words = bad_words.union(v)
    result = list(bad_words)
    result.sort()
    with open(TYPO_WORDS_FILE, "w") as t:
        l = list()
        for i in result:
            l.append(i)
            if len(" ".join(l)) >= 80:
                t.write(" ".join(l) + "\n")
                l = list()
                continue
        else:
            t.write(" ".join(l) + "\n")


def get_projects(project="kubernetes"):
    if project == "kubernetes":
        return "/home/matrix/go/src/k8s.io/kubernetes"
    elif project == "prometheus":
        return "/home/matrix/go/src/github.com/prometheus/prometheus"
    else:
        # helm envoy fluentd coredns containerd tikv etcd
        return os.path.join("/home/matrix/workspace/github", project)


if __name__ == "__main__":
    project = get_projects()
    # run_file_ext_statistics(project=project)
    run_spell_check(project=project)
    save_typo_words()
    print_cache()