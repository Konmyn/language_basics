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
# print(df)

# 复权因子
# https://tushare.pro/document/2?doc_id=28
# df = pro.adj_factor(ts_code='000001.SZ', trade_date='')
# print(df)


