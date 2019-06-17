import numpy as np
import pandas
import tushare as ts
from datetime import datetime
from pathlib import Path
import matplotlib.pyplot as plt


token = open("token.txt", "r").readline().strip()
ts.set_token(token)

pro = ts.pro_api()
now_date_str = datetime.now().strftime("%Y%m%d")


# 交易日历
# https://tushare.pro/document/2?doc_id=26
# df = pro.trade_cal(exchange='', start_date='20180901', end_date='20181001', fields='exchange,cal_date,is_open,pretrade_date', is_open='0')
# 交易所 SSE上交所 SZSE深交所
# 是否交易 '0'休市 '1'交易
def get_calender():
    calender_file = 'data/shanghai-calender-{}.csv'.format(now_date_str)
    my_file = Path(calender_file)
    if my_file.is_file():
        shanghai = pandas.read_csv(calender_file, index_col=0)
        shanghai["cal_date"] = shanghai["cal_date"].astype(str)
    else:
        shanghai = pro.trade_cal(exchange='SSE', start_date='19900101', end_date='20200101')
        shanghai.to_csv(calender_file)
    return shanghai
    # shenzhen = pro.trade_cal(exchange='SZSE', start_date='19900101', end_date='20200101')
    # shenzhen.to_csv('shenzhen-calender-{}.csv'.format(now_date_str))
    # for index, row in shanghai.iterrows():
    #     print(row["cal_date"])
    #     print(index)
    #     print(shenzhen.loc[[index]]["cal_date"])
    #     break
    # print(shanghai)
    # print(shenzhen)

# scatter is not working for non numeric data
# get_calender().plot.scatter(x="cal_date", y="is_open")

# get_calender().plot.line(x="cal_date", y="is_open")

# just plot is ok
# get_calender().plot(x="cal_date", y="is_open", style='o')
# plt.show()


# 股票列表
# https://tushare.pro/document/2?doc_id=25
# data = pro.query('stock_basic', exchange='', list_status='L', fields='ts_code,symbol,name,area,industry,list_date')
# data = pro.stock_basic(exchange='', list_status='L')
# print(data)
def stock_list():
    stock_list_file = 'data/stock-list-{}.csv'.format(now_date_str)
    my_file = Path(stock_list_file)
    if my_file.is_file():
        # https://stackoverflow.com/questions/49684951/pandas-read-csv-dtype-read-all-columns-but-few-as-string
        stocks = pandas.read_csv(stock_list_file, index_col=0, dtype=str)
    else:
        stocks = pro.stock_basic()
        stocks.to_csv(stock_list_file)
    return stocks

# print(stock_list().info())


# 股票曾用名
# https://tushare.pro/document/2?doc_id=100
# df = pro.namechange(ts_code='600848.SH', fields='ts_code,name,start_date,end_date,change_reason')
# df = pro.namechange(ts_code='600848.SH')
# print(df)

def _former_name_web(code):
    name_list = pro.namechange(ts_code=code)
    return name_list

def former_name(code):
    former_name_file = 'data/former-name-{}-{}.csv'.format(code, now_date_str)
    my_file = Path(former_name_file)
    if my_file.is_file():
        name_list = pandas.read_csv(former_name_file, index_col=0, dtype=str)
    else:
        name_list = _former_name_web(code)
        name_list.to_csv(former_name_file)
    return name_list


# print(former_name('600848.SH'))


# 沪深股通成份股
# https://tushare.pro/document/2?doc_id=104
# # 获取沪股通成分
# df = pro.hs_const(hs_type='SH')
# print(df)
# # 获取深股通成分
# df = pro.hs_const(hs_type='SZ')
# print(df)
def shanghai_hongkong_stock():
    stock_list_file = 'data/shanghai-hongkong-stock-{}.csv'.format(now_date_str)
    my_file = Path(stock_list_file)
    if my_file.is_file():
        name_list = pandas.read_csv(stock_list_file, index_col=0, dtype=str)
    else:
        name_list = pro.hs_const(hs_type='SH')
        name_list.to_csv(stock_list_file)
    return name_list

# print(shanghai_hongkong_stock())
# print(shanghai_hongkong_stock().info())

def shenzhen_hongkong_stock():
    stock_list_file = 'data/shenzhen-hongkong-stock-{}.csv'.format(now_date_str)
    my_file = Path(stock_list_file)
    if my_file.is_file():
        name_list = pandas.read_csv(stock_list_file, index_col=0, dtype=str)
    else:
        name_list = pro.hs_const(hs_type='SZ')
        name_list.to_csv(stock_list_file)
    return name_list

# print(shenzhen_hongkong_stock())
# print(shenzhen_hongkong_stock().info())


# 上市公司基本信息
# https://tushare.pro/document/2?doc_id=112
# 交易所代码 ，SSE上交所 SZSE深交所 ，默认SSE
# df = pro.stock_company(exchange='SZSE', fields='ts_code,chairman,manager,secretary,reg_capital,setup_date,province')
# df = pro.stock_company(exchange='SZSE')
# # print(df.columns)
# print(df)
def stock_company_basic_info(loc):
    company_info_file = 'data/company-info-{}-{}.csv'.format(loc, now_date_str)
    my_file = Path(company_info_file)
    if my_file.is_file():
        name_list = pandas.read_csv(company_info_file, index_col=0, dtype=str)
    else:
        name_list = pro.stock_company(exchange=loc)
        name_list["reg_capital"] = name_list["reg_capital"].astype(str)
        name_list["employees"] = name_list["employees"].astype(str)
        name_list.to_csv(company_info_file)
    return name_list

# print(stock_company_basic_info("SSE").info())
# print(stock_company_basic_info("SZSE").info())


# IPO新股列表
# 限量：单次最大2000条，总量不限制
# https://tushare.pro/document/2?doc_id=123
# 经测试接口数据是从2008年开始的
# df = pro.new_share(start_date='20080101', end_date='20150101')
# df = pro.new_share(start_date='20150101', end_date='20200101')
# print(df)
def new_stock_list():
    new_stock_file = 'data/new-stock-info-{}.csv'.format(now_date_str)
    my_file = Path(new_stock_file)
    if my_file.is_file():
        name_list = pandas.read_csv(new_stock_file, index_col=0, dtype=str)
        name_list["amount"] = name_list["amount"].astype(float)
        name_list["market_amount"] = name_list["market_amount"].astype(float)
        name_list["price"] = name_list["price"].astype(float)
        name_list["pe"] = name_list["pe"].astype(float)
        name_list["limit_amount"] = name_list["limit_amount"].astype(float)
        name_list["funds"] = name_list["funds"].astype(float)
        name_list["ballot"] = name_list["ballot"].astype(float)
    else:
        df1 = pro.new_share(start_date='20080101', end_date='20150101')
        df2 = pro.new_share(start_date='20150101', end_date=now_date_str)
        name_list = pandas.concat([df1, df2]).reset_index(drop=True)
        name_list.to_csv(new_stock_file)
    return name_list

# print(new_stock_list().iloc[[0, -1]])
# print(new_stock_list().info())


# 日线行情
# https://tushare.pro/document/2?doc_id=27
# df = pro.daily(ts_code='000001.SZ', start_date='20180701', end_date='20180718')
# df = pro.daily(ts_code='000001.SZ')
# print(df.info())

def daily_k_line(code):
    daily_k_line_file = 'data/daily-k-{}-{}.csv'.format(code, now_date_str)
    my_file = Path(daily_k_line_file)
    if my_file.is_file():
        name_list = pandas.read_csv(daily_k_line_file, index_col=0, dtype=str)
        name_list["open"] = name_list["open"].astype(float)
        name_list["high"] = name_list["high"].astype(float)
        name_list["low"] = name_list["low"].astype(float)
        name_list["close"] = name_list["close"].astype(float)
        name_list["pre_close"] = name_list["pre_close"].astype(float)
        name_list["change"] = name_list["change"].astype(float)
        name_list["pct_chg"] = name_list["pct_chg"].astype(float)
        name_list["vol"] = name_list["vol"].astype(float)
        name_list["amount"] = name_list["amount"].astype(float)
    else:
        name_list = pro.daily(ts_code=code)
        name_list.to_csv(daily_k_line_file)
    return name_list

# print(daily_k_line('000001.SZ'))


def close_price_line():
    # simple line plot, it's too slow
    stock = daily_k_line('000001.SZ')
    # https://stackoverflow.com/questions/20444087/right-way-to-reverse-pandas-dataframe
    stock = stock.reindex(index=stock.index[::-1])
    plt.plot(stock["trade_date"], stock["close"])
    plt.xticks(rotation=90)
    plt.xlabel("date")
    plt.ylabel("price")
    plt.title("000001.SZ")
    plt.show()

# close_price_line()


def daily_k_all(date):
    # 不需要用请求时间进行标记
    daily_k_all_file = 'data/daily-k-all-{}.csv'.format(date)
    my_file = Path(daily_k_all_file)
    if my_file.is_file():
        name_list = pandas.read_csv(daily_k_all_file, index_col=0, dtype=str)
        name_list["open"] = name_list["open"].astype(float)
        name_list["high"] = name_list["high"].astype(float)
        name_list["low"] = name_list["low"].astype(float)
        name_list["close"] = name_list["close"].astype(float)
        name_list["pre_close"] = name_list["pre_close"].astype(float)
        name_list["change"] = name_list["change"].astype(float)
        name_list["pct_chg"] = name_list["pct_chg"].astype(float)
        name_list["vol"] = name_list["vol"].astype(float)
        name_list["amount"] = name_list["amount"].astype(float)
    else:
        name_list = pro.daily(trade_date=date)
        name_list.to_csv(daily_k_all_file)
    return name_list


def scatter_with_histgram():
    # Fixing random state for reproducibility
    np.random.seed(19680801)

    kinfo = daily_k_all('20190612')
    close_prices = kinfo["close"].values
    pct_changes = kinfo["pct_chg"].values
    x = kinfo["close"].values
    y = kinfo["pct_chg"].values

    # definitions for the axes
    left, width = 0.1, 0.65
    bottom, height = 0.1, 0.65
    spacing = 0.005

    rect_scatter = [left, bottom, width, height]
    rect_histx = [left, bottom + height + spacing, width, 0.2]
    rect_histy = [left + width + spacing, bottom, 0.2, height]

    # start with a rectangular Figure
    plt.figure(figsize=(8, 8))

    ax_scatter = plt.axes(rect_scatter)
    ax_scatter.tick_params(direction='in', top=True, right=True)
    ax_histx = plt.axes(rect_histx)
    ax_histx.tick_params(direction='in', labelbottom=False)
    ax_histy = plt.axes(rect_histy)
    ax_histy.tick_params(direction='in', labelleft=False)


    # the scatter plot:
    ax_scatter.scatter(x, y)

    # now determine nice limits by hand:
    binwidth = 0.25
    lim = np.ceil(np.abs([x, y]).max() / binwidth) * binwidth
    x_lim = lim
    y_lim = 11
    # ax_scatter.set_xlim((-5, lim))
    ax_scatter.set_ylim((-y_lim, y_lim))

    ax_scatter.semilogx([1, 10, 100, 1000], [1, 10, 100, 1000])

    bins = np.arange(-lim, lim + binwidth, binwidth)
    ax_histx.hist(x, bins=bins)
    ax_histy.hist(y, bins=bins, orientation='horizontal')

    ax_histx.set_xlim(ax_scatter.get_xlim())
    ax_histx.semilogx([1, 10, 100], [1, 10, 100])
    ax_histy.set_ylim(ax_scatter.get_ylim())

    plt.show()

# scatter_with_histgram()

# A股复权行情
# https://tushare.pro/document/2?doc_id=146
#取000001的前复权行情
# df = ts.pro_bar(ts_code='000001.SZ', adj='qfq', end_date='20190612')
# print(df)
# #取000001的后复权行情
# df = ts.pro_bar(ts_code='000001.SZ', adj='hfq', start_date='20180101', end_date='20181011')
# print(df)
# 前复权，以当天为基准
def adjusted_daily_k_line(code):
    adjusted_daily_k_line_file = 'data/adjusted-daily-k-{}-{}.csv'.format(code, now_date_str)
    my_file = Path(adjusted_daily_k_line_file)
    if my_file.is_file():
        name_list = pandas.read_csv(adjusted_daily_k_line_file, index_col=0, dtype=str)
        name_list["open"] = name_list["open"].astype(float)
        name_list["high"] = name_list["high"].astype(float)
        name_list["low"] = name_list["low"].astype(float)
        name_list["close"] = name_list["close"].astype(float)
        name_list["pre_close"] = name_list["pre_close"].astype(float)
        name_list["change"] = name_list["change"].astype(float)
        name_list["pct_chg"] = name_list["pct_chg"].astype(float)
        name_list["vol"] = name_list["vol"].astype(float)
        name_list["amount"] = name_list["amount"].astype(float)
    else:
        name_list = ts.pro_bar(ts_code=code, adj='qfq', end_date=now_date_str)
        name_list.to_csv(adjusted_daily_k_line_file)
    return name_list

# print(adjusted_daily_k_line('000001.SZ').info())


# 复权因子
# https://tushare.pro/document/2?doc_id=28
# df = pro.adj_factor(ts_code='000001.SZ', trade_date='')
# print(df)


def adjust_factor(code):
    adjusted_factor_file = 'data/adjusted-factor-{}-{}.csv'.format(code, now_date_str)
    my_file = Path(adjusted_factor_file)
    if my_file.is_file():
        name_list = pandas.read_csv(adjusted_factor_file, index_col=0, dtype=str)
        name_list["adj_factor"] = name_list["adj_factor"].astype(float)
    else:
        name_list = pro.adj_factor(ts_code=code)
        name_list.to_csv(adjusted_factor_file)
    return name_list


# print(adjust_factor('000001.SZ').info())


# 每日指标
# https://tushare.pro/document/2?doc_id=32
# df = pro.daily_basic(ts_code='', trade_date='20180726', fields='ts_code,trade_date,turnover_rate,volume_ratio,pe,pb')
# df = pro.daily_basic(trade_date='20180726')
# print(df)


def daily_technical_all(date):
    # 不需要用请求时间进行标记
    daily_technical_all_file = 'data/daily-technical-all-{}.csv'.format(date)
    my_file = Path(daily_technical_all_file)
    if my_file.is_file():
        name_list = pandas.read_csv(daily_technical_all_file, index_col=0)
        name_list["trade_date"] = name_list["trade_date"].astype(str)
    else:
        name_list = pro.daily_basic(trade_date=date)
        name_list.to_csv(daily_technical_all_file)
    return name_list


# print(daily_technical_all('20180726').head())


# 指数基本信息
# https://tushare.pro/document/2?doc_id=94
# MSCI 	MSCI指数
# CSI 	中证指数
# SSE 	上交所指数
# SZSE 	深交所指数
# CICC 	中金所指数
# SW 	申万指数
# OTH 	其他指数
# df = pro.index_basic(market='SW')
# print(df)


def index_basic_info(mkt):
    index_basic_info_file = 'data/index-basic-info-{}-{}.csv'.format(mkt, now_date_str)
    my_file = Path(index_basic_info_file)
    if my_file.is_file():
        name_list = pandas.read_csv(index_basic_info_file, index_col=0, dtype=str)
        name_list["base_point"] = name_list["base_point"].astype(float)
    else:
        name_list = pro.index_basic(market=mkt)
        name_list.to_csv(index_basic_info_file)
    return name_list


# print(index_basic_info('SW').info())

# 指数日线行情
# https://tushare.pro/document/2?doc_id=95

# df = pro.index_daily(ts_code='000001.SH')
# print(df)


def index_k_line(code):
    index_k_line_file = 'data/index-k-line-{}-{}.csv'.format(code, now_date_str)
    my_file = Path(index_k_line_file)
    if my_file.is_file():
        name_list = pandas.read_csv(index_k_line_file, index_col=0)
        name_list["trade_date"] = name_list["trade_date"].astype(str)
    else:
        name_list = pro.index_daily(ts_code=code)
        name_list.to_csv(index_k_line_file)
    return name_list


# print(index_k_line('000001.SH').info())


# 大盘指数每日指标
# https://tushare.pro/document/2?doc_id=128
# 目前只提供上证综指，深证成指，上证50，中证500，中小板指，创业板指的每日指标数据
# df = pro.index_dailybasic(trade_date='20181018', fields='ts_code,trade_date,turnover_rate,pe')
# df = pro.index_dailybasic(trade_date='20181018')
# print(df)


def index_technical(date):
    index_technical_file = 'data/index-technical-{}.csv'.format(date)
    my_file = Path(index_technical_file)
    if my_file.is_file():
        name_list = pandas.read_csv(index_technical_file, index_col=0)
        name_list["trade_date"] = name_list["trade_date"].astype(str)
    else:
        name_list = pro.index_dailybasic(trade_date=date)
        name_list.to_csv(index_technical_file)
    return name_list


# print(index_technical("20181018").info())


# 指数成分和权重
# https://tushare.pro/document/2?doc_id=96

# df = pro.index_weight(index_code='000001.SH', start_date='20180901', end_date='20180930')
# df = pro.index_weight(index_code='000001.SH')
# print(df)

