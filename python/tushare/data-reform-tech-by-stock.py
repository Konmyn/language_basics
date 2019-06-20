import time
import os
import pandas
import tushare as ts
from datetime import datetime
from pathlib import Path

token = open("token.txt", "r").readline().strip()
ts.set_token(token)

pro = ts.pro_api()
now_str = datetime.now().strftime("%Y%m%d")

root_path = "/home/matrix/workspace/stock-data"

# 分日技术指标
daily_technical_path = "daily-technical"
daily_technical_file = "daily-technical-all-{}.csv"

# 股市日历
calender_path = "calender-sh"
calender_file = "shanghai-calender-{}.csv"

# 股票列表
list_path = "stock-list"
list_file = "stock-list-{}.csv"

# 股票指标列表
tech_path = "stock-tech"
tech_file = "stock-tech-{}.csv"

# 缓存
cache = dict()


def timer(func):
    def wrapper(*args, **kwargs):
        before = time.time()
        print("runing", func.__name__, *args, **kwargs)
        print("docs", func.__doc__)
        result = func(*args, **kwargs)
        after = time.time()
        print("runing", func.__name__, "time used:", after - before)
        return result
    return wrapper


@timer
def stock_list():
    """
    获取今日的股票列表
    """
    if "stock_list" in cache:
        return cache["stock_list"]
    f = list_file.format(now_str)
    file_path = os.path.join(root_path, list_path, f)
    my_file = Path(file_path)
    if my_file.is_file():
        stocks = pandas.read_csv(file_path, index_col=0, dtype=str)
    else:
        stocks = pro.stock_basic()
        stocks.to_csv(file_path)
    cache["stock_list"] = stocks
    return stocks


@timer
def get_calender():
    """
    获取股市日历
    """
    if "stock_calender" in cache:
        return cache["stock_calender"]
    f = daily_technical_file.format(now_str)
    file_path = os.path.join(root_path, calender_path, f)
    my_file = Path(file_path)
    if my_file.is_file():
        df = pandas.read_csv(file_path, index_col=0)
        df["cal_date"] = df["cal_date"].astype(str)
    else:
        df = pro.trade_cal(exchange='SSE', start_date='19900101', end_date=now_str)
        df.to_csv(file_path)
    # 如果时间太早，则删掉今天
    if datetime.now().hour < 17:
        df.drop(df.tail(1).index, inplace=True)
    cache["stock_calender"] = df
    return df


def stock_base_info(code):
    slist = stock_list()
    slist = slist.set_index("symbol")
    info = slist.loc[[code]]
    # print(info.info())
    print(info.get("list_date").item())
    return info


tech_columns = ['trade_date', 'close', 'turnover_rate', 'turnover_rate_f',
       'volume_ratio', 'pe', 'pe_ttm', 'pb', 'ps', 'ps_ttm', 'total_share',
       'float_share', 'free_share', 'total_mv', 'circ_mv']


@timer
def get_stock_technical(code):
    """
    获取并更新股票的技术指标
    """
    info = stock_base_info(code)
    calender = get_calender()
    full_data = load_stock_tech(code)
    list_date = info.get("list_date").item()
    if full_data is None:
        updated_to = "19900101"
    else:
        updated_to = full_data.index[-1]

    updated = False
    for index, row in calender.iterrows():
        if row["cal_date"] < list_date or row["cal_date"] <= updated_to:
            continue
        if row["is_open"] == 0:
            continue
        date = row["cal_date"]
        all_data = daily_technical_all(date)
        all_data.ts_code = all_data.ts_code.str[:6]
        all_data = all_data.set_index("ts_code")
        try:
            day_info = all_data.loc[[code]]
        except KeyError:
            print(code, "in", date, "no data")
            day_info = pandas.DataFrame(columns=tech_columns)
            day_info.loc[code] = [date] + ([None] * (len(tech_columns) - 1))
        if full_data is None:
            full_data = day_info.set_index("trade_date")
        else:
            full_data = full_data.append(day_info.set_index("trade_date"))
        updated = True
    # full_data = full_data.set_index("trade_date")
    # print(full_data)
    if updated:
        save_stock_tech(code, full_data)
    return full_data


def daily_technical_all(date):
    if date in cache:
        return cache[date]

    f = daily_technical_file.format(date)
    file_path = os.path.join(root_path, daily_technical_path, f)
    my_file = Path(file_path)
    if my_file.is_file():
        name_list = pandas.read_csv(file_path, index_col=0)
        name_list["trade_date"] = name_list["trade_date"].astype(str)
    else:
        name_list = pro.daily_basic(trade_date=date)
        name_list.to_csv(file_path)
    cache[date] = name_list
    return name_list


def load_stock_tech(code):
    f = tech_file.format(code)
    file_path = os.path.join(root_path, tech_path, f)
    my_file = Path(file_path)
    if my_file.is_file():
        name_list = pandas.read_csv(file_path, index_col=0)
        # name_list["trade_date"] = name_list["trade_date"].astype(str)
        name_list.index = name_list.index.map(str)
        return name_list
    else:
        return None


def save_stock_tech(code, data):
    f = tech_file.format(code)
    file_path = os.path.join(root_path, tech_path, f)
    return data.to_csv(file_path)


def get_all_stock_technical():
    slist = stock_list()
    for index, row in slist.iterrows():
        get_stock_technical(row["symbol"])


if __name__ == "__main__":
    get_all_stock_technical()
    # print(get_calender())
