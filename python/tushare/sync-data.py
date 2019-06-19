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


def timer(func):
    def wrapper(*args, **kwargs):
        before = time.time()
        result = func(*args, **kwargs)
        after = time.time()
        print("time used:", after - before)
        return result
    return wrapper


def get_calender():
    f = daily_technical_file.format(now_str)
    file_path = os.path.join(root_path, calender_path, f)
    my_file = Path(file_path)
    if my_file.is_file():
        shanghai = pandas.read_csv(file_path, index_col=0)
        shanghai["cal_date"] = shanghai["cal_date"].astype(str)
    else:
        shanghai = pro.trade_cal(exchange='SSE', start_date='19900101', end_date=now_str)
        shanghai.to_csv(file_path)
    return shanghai


def daily_technical_all(date):
    f = daily_technical_file.format(date)
    file_path = os.path.join(root_path, daily_technical_path, f)
    my_file = Path(file_path)
    if my_file.is_file():
        return
    else:
        name_list = pro.daily_basic(trade_date=date)
        name_list.to_csv(file_path)
        return


def stock_list():
    f = list_file.format(now_str)
    file_path = os.path.join(root_path, list_path, f)
    my_file = Path(file_path)
    if my_file.is_file():
        return
    else:
        stocks = pro.stock_basic()
        stocks.to_csv(file_path)
        return


def get_all_technical():
    calender = get_calender()
    # https://cmdlinetips.com/2018/12/how-to-loop-through-pandas-rows-or-how-to-iterate-over-pandas-rows/
    for index, row in calender.iterrows():
        # Exception: 抱歉，您每分钟最多访问该接口200次，权限的具体详情访问：https://tushare.pro/document/1?doc_id=108。
        # 只有第一次会碰到这个问题，以后增量更新时应该不会遇到这种问题
        # requests.exceptions.ConnectionError: HTTPConnectionPool(host='api.waditu.com', port=80): Read timed out.
        if row["is_open"] == 1:
            print(row["cal_date"])
            try:
                daily_technical_all(row["cal_date"])
            except Exception as e:
                print(e)
                raise e
        else:
            continue


@timer
def run():
    get_all_technical()
    stock_list()


if __name__ == "__main__":
    run()
