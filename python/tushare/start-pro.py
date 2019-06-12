import tushare as ts

token = open("token.txt", "r").readline().strip()
ts.set_token(token)

pro = ts.pro_api()

# 交易日历
# https://tushare.pro/document/2?doc_id=26
# df = pro.trade_cal(exchange='', start_date='20180901', end_date='20181001', fields='exchange,cal_date,is_open,pretrade_date', is_open='0')
# df = pro.trade_cal(start_date='20050101', end_date='20200101')
# print(df)

# 股票列表
# https://tushare.pro/document/2?doc_id=25
# data = pro.query('stock_basic', exchange='', list_status='L', fields='ts_code,symbol,name,area,industry,list_date')
# data = pro.stock_basic(exchange='', list_status='L')
# print(data)

# 股票曾用名
# https://tushare.pro/document/2?doc_id=100
# df = pro.namechange(ts_code='600848.SH', fields='ts_code,name,start_date,end_date,change_reason')
# df = pro.namechange(ts_code='600848.SH', fields='ts_code,name,start_date,end_date,change_reason')
# print(df)

# 沪深股通成份股
# https://tushare.pro/document/2?doc_id=104
# # 获取沪股通成分
# df = pro.hs_const(hs_type='SH')
# print(df)
# # 获取深股通成分
# df = pro.hs_const(hs_type='SZ')
# print(df)

# 上市公司基本信息
# https://tushare.pro/document/2?doc_id=112
# df = pro.stock_company(exchange='SZSE', fields='ts_code,chairman,manager,secretary,reg_capital,setup_date,province')
# df = pro.stock_company(exchange='SZSE')
# # print(df.columns)
# print(df)

# 日线行情
# https://tushare.pro/document/2?doc_id=27
# df = pro.daily(ts_code='000001.SZ', start_date='20180701', end_date='20180718')
# print(df)

# 复权因子
# https://tushare.pro/document/2?doc_id=28
# df = pro.adj_factor(ts_code='000001.SZ', trade_date='')
# print(df)


