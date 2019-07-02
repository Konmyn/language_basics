from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
import pandas as pd
from datetime import datetime
from collections import defaultdict

from .forms import KeyForm
from .helper import get_word_cloud_by_freq


# 每日关键词输入
def keyin(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = KeyForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # print(form.cleaned_data)
            # print(type(form.cleaned_data)) # dict
            df = pd.DataFrame(form.cleaned_data, index=[datetime.now().strftime("%Y-%m-%d")])
            df.to_csv("key_info.csv")
            return HttpResponseRedirect('/info/')

    # if a GET (or any other method) we'll create a blank form
    else:
        df = pd.read_csv("key_info.csv", index_col=0, dtype=str)
        if datetime.now().strftime("%Y-%m-%d") in df.index:
            return HttpResponseRedirect('/info/')
        # print(df.loc["2019-07-02"])
        # print(df.info())
        form = KeyForm()
    # https://simpleisbetterthancomplex.com/tutorial/2018/11/28/advanced-form-rendering-with-django-crispy-forms.html
    return render(request, 'keyin.html', {'form': form})


# 关键词综合信息展示
def info(request):
    df = pd.read_csv("key_info.csv", index_col=0, dtype=str)
    return HttpResponse(df.to_html())


# 关键词词云
def cloud(request):
    df = pd.read_csv("key_info.csv", index_col=0, dtype=str)
    freq = defaultdict(int)
    for index, row in df.iterrows():
        if row["primary_key"]:
            freq[row["primary_key"]] += 8
        if row["secondary_key"]:
            freq[row["secondary_key"]] += 4
        if row["ternary_key"]:
            freq[row["ternary_key"]] += 2
        if row["quartus_key"]:
            freq[row["quartus_key"]] += 1
        if row["fifth_key"]:
            freq[row["fifth_key"]] += 1
    # print(freq)
    wc = get_word_cloud_by_freq(freq)
    image = wc.to_image()
    # print(dir(image))
    # image.show()  # can work
    response = HttpResponse(content_type="image/png")
    image.save(response, "PNG")
    return response

