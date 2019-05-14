#! /usr/bin/env python3

from jinja2 import Environment, FileSystemLoader


def load_templates():
    file_loader = FileSystemLoader(".")
    env = Environment(loader=file_loader)
    template = env.get_template("apollo.conf.template")
    return template


def load_configs():
    return [
        {"appid": 1, "randomstr": "a"},
        {"appid": 3, "randomstr": "y"},
        {"appid": 2, "randomstr": "x"},
    ]


def gen_nginx_conf(output=None):
    # print(output)
    with open("apollo.conf", "w") as f:
        f.write(output)
    return True


def run():
    template = load_templates()
    datas = load_configs()
    datas.sort(key=lambda x: x["appid"])
    output = template.render(datas=datas)
    result = gen_nginx_conf(output)
    assert result == True


if __name__ == "__main__":
    run()
