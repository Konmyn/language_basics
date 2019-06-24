import time
import os
import pandas
import tushare as ts
from datetime import datetime
from pathlib import Path
import logging
from collections import defaultdict

logFormatter = '%(asctime)s - %(levelname)s - %(name)s:%(lineno)d - %(message)s'
logging.basicConfig(format=logFormatter, level=logging.INFO)
logger = logging.getLogger(__name__)

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

# 股票指标列表
tech_path_new = "stock-tech-new"
tech_file_new = "{}.csv"

# 缓存
cache = defaultdict(list)


def timer(func):
    def wrapper(*args, **kwargs):
        before = time.time()
        logger.info("runing %s %s %s" % (func.__name__, args, kwargs))
        logger.info("docs %s" % func.__doc__)
        result = func(*args, **kwargs)
        after = time.time()
        logger.info("runing %s time used: %s" % (func.__name__, after - before))
        return result
    return wrapper


@timer
def stock_list():
    """
    获取今日的股票列表
    """
    f = list_file.format(now_str)
    file_path = os.path.join(root_path, list_path, f)
    my_file = Path(file_path)
    if my_file.is_file():
        stocks = pandas.read_csv(file_path, index_col=0, dtype=str)
    else:
        stocks = pro.stock_basic()
        stocks.to_csv(file_path)
    return stocks


@timer
def get_calender():
    """
    获取股市日历
    """
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
    return df


def stock_base_info(code):
    slist = stock_list()
    slist = slist.set_index("symbol")
    info = slist.loc[[code]]
    # logger.info(info.info())
    # logger.info(info.get("list_date").item())
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
            logger.info("%s in %s no data" % code, date)
            day_info = pandas.DataFrame(columns=tech_columns)
            day_info.loc[code] = [date] + ([None] * (len(tech_columns) - 1))
        if full_data is None:
            full_data = day_info.set_index("trade_date")
        else:
            full_data = full_data.append(day_info.set_index("trade_date"))
        updated = True
    # full_data = full_data.set_index("trade_date")
    # logger.info(full_data)
    if updated:
        save_stock_tech(code, full_data)
    return full_data


def daily_technical_all(date):
    f = daily_technical_file.format(date)
    file_path = os.path.join(root_path, daily_technical_path, f)
    my_file = Path(file_path)
    if my_file.is_file():
        name_list = pandas.read_csv(file_path, index_col=0)
        name_list["trade_date"] = name_list["trade_date"].astype(str)
    else:
        name_list = pro.daily_basic(trade_date=date)
        name_list.to_csv(file_path)
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


@timer
def reformer():
    """把每日的技术分析转换为每股的技术分析"""
    logger.info("prepare common data")
    calender = get_calender()
    logger.info("prepare reformed data")
    for index, row in calender.iterrows():
        date = row["cal_date"]
        if row["is_open"] == 0:
            continue
        before = time.time()
        logger.info("stock data in %s" % date)
        daily_tech_data = daily_technical_all(date)
        for dindex, drow in daily_tech_data.iterrows():
            cache[drow["ts_code"]].append(drow)
        after = time.time()
        logger.info("time cost %s" % (after - before))

    logger.info("prepare to save data")
    for i in cache:
        logger.info("saving %s data" % i)
        before = time.time()
        df = pandas.DataFrame(cache.pop(i))
        save_stock_tech_new(i, df)
        after = time.time()
        logger.info("time cost %s" % (after - before))

    logger.info("all done")


def save_stock_tech_new(code, data):
    f = tech_file_new.format(code)
    file_path = os.path.join(root_path, tech_path_new, f)
    return data.to_csv(file_path)


# 这个脚本要运行大概4个小时，简直无法忍受
# 2019-06-21 16:55:35,084 - INFO - saving 603999 data
# 2019-06-21 16:55:35,097 - INFO - all done
# 2019-06-21 16:55:35,097 - INFO - error code: {'600832', '002604', '000916', '600899', '600001', '000618', '600087', '600878', '600296', '000024', '000562', '000022', '600625', '600656', '600806', '000765', '600003', '600700', '000748', '000658', '600799', '000979', '600253', '600627', '300186', '000956', '600852', '601299', '000522', '600270', '000787', '600659', '600670', '000406', '000047', '000939', '000033', '000769', '600842', '600669', '000515', '000699', '300372', '002680', '600607', '000588', '600092', '600762', '600752', '000578', '600005', '600991', '000689', '000569', '600672', '000730', '600002', '000832', '600263', '000621', '000866', '000015', '000508', '002070', '000602', '600205', '600357', '600813', '300216', '603217', '000817', '000511', '000995', '000827', '600646', '000535', '600632', '000660', '000003', '000527', '600788', '000763', '000805', '600772', '000549', '002260', '000013', '600680', '600286', '600181', '600553', '601268', '000405', '000594', '600102', '600709', '000583', '600591', '300028', '600631', '000693', '000412', '600840', '600065', '000542', '300104', '600472', '000556', '600432', '000675', '000653', '600786'}


# 新的脚本比较消耗内存，16G吃满，但耗时有明显降低：
# runing reformer time used: 1982.0495052337646

if __name__ == "__main__":
    # get_all_stock_technical()
    # logger.info(get_calender())
    reformer()
