# https://blog.csdn.net/u014281392/article/details/73611624
import baostock as bs
import pandas as pd
import matplotlib as mpl
import tushare as ts
import matplotlib.pyplot as plt
import mpl_finance as mpf
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()

# https://www.cnblogs.com/hhh5460/p/4323985.html
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

#### 登陆系统 ####
lg = bs.login()
# 显示登陆返回信息
print('login respond error_code:'+lg.error_code)
print('login respond  error_msg:'+lg.error_msg)

#### 获取沪深A股历史K线数据 ####
# 详细指标参数，参见“历史行情指标参数”章节；“分钟线”参数与“日线”参数不同。
rs = bs.query_history_k_data_plus("sh.600000",
    "date,open,high,low,close,volume,amount,code,preclose,adjustflag,turn,tradestatus,pctChg,isST",
    start_date='2017-07-01', end_date='2017-12-31',
    frequency="d", adjustflag="3")
print('query_history_k_data_plus respond error_code:'+rs.error_code)
print('query_history_k_data_plus respond  error_msg:'+rs.error_msg)

#### 打印结果集 ####
data_list = []
while (rs.error_code == '0') & rs.next():
    # 获取一条记录，将记录合并在一起
    data_list.append(rs.get_row_data())
result = pd.DataFrame(data_list, columns=rs.fields)

result['open'] = result['open'].astype(float)
result['high'] = result['high'].astype(float)
result['low'] = result['low'].astype(float)
result['close'] = result['close'].astype(float)
result['preclose'] = result['preclose'].astype(float)
result['volume'] = result['volume'].astype(float)
result['amount'] = result['amount'].astype(float)
result['turn'] = result['turn'].astype(float)
result['pctChg'] = result['pctChg'].astype(float)

#### 结果集输出到csv文件 ####
result.to_csv("history_A_stock_k_data.csv", index=False)
print(result)
print(result.info())

#### 登出系统 ####
bs.logout()

# 导入两个涉及的库
from matplotlib.pylab import date2num
import datetime

# 对tushare获取到的数据转换成candlestick_ohlc()方法可读取的格式
'''
data_list = []
for dates,row in hist_data.iterrows():
    # 将时间转换为数字
    date_time = datetime.datetime.strptime(dates,'%Y-%m-%d')
    t = date2num(date_time)
    open,high,low,close = row[:4]
    datas = (t,open,high,low,close)
    data_list.append(datas)
'''

def date_to_num(dates):
    num_time = []
    for date in dates:
        date_time = datetime.datetime.strptime(date, '%Y-%m-%d')
        num_date = date2num(date_time)
        num_time.append(num_date)
    return num_time
# dataframe转换为二维数组

mat_wdyx = result.values
num_time = date_to_num(mat_wdyx[:, 0])
mat_wdyx[:, 0] = num_time
# 日期, 开盘, 收盘, 最高, 最低, 成交量, 代码
print(mat_wdyx[:3])

fig, ax = plt.subplots(figsize=(15, 5))
fig.subplots_adjust(bottom=0.5)
mpf.candlestick_ochl(ax, mat_wdyx, width=0.6, colorup='r', colordown='g')
plt.grid(True)
# 设置日期刻度旋转的角度
plt.xticks(rotation=30)
plt.title('wandayuanxian')
plt.xlabel('Date')
plt.ylabel('Price')
# x轴的刻度为日期
ax.xaxis_date()
###candlestick_ochl()函数的参数
# ax 绘图Axes的实例
# mat_wdyx 价格历史数据
# width    图像中红绿矩形的宽度,代表天数
# colorup  收盘价格大于开盘价格时的颜色
# colordown   低于开盘价格时矩形的颜色
# alpha      矩形的颜色的透明度
plt.show()
