import easytrader
import easyquotation
import time
import datetime
import sqlite3
from tkinter import *       #引用Tk模块
import tkinter.messagebox
import urllib.request
#import sinaquotationsz


class IndexData:
    ID = 0
    Code = 0
    Price = 0
    Date = ''
    Time = ''
    KEMA = 0
    SEMA = 0
    LEMA = 0
    DIF = 0
    xlA = 0
    xlB = 0
    xlC = 0
    IsHold = 0
    KEMAH = 0
    PriceH = 0
    DEA = 0
    BuyToday = 0
    # 定义基本属性

data_dict_sample ={'ID':1,
              'Code':510050,
              'Price':0.123,
              'Date':'2016-01-01',
              'Time':'12:12:12',
              'KEMA':0.123,
              'SEMA':0.123,
              'LEMA':0.123,
              'DIF':0.123,
              'xlA':0.123,
              'xlB':0.123,
              'xlC':0.123,
              'IsHold':0,
              'KEMAH':0.123,
              'PriceH':0.123,
              'DEA':0.123,
              'BuyToday':1}

def creat_table():  #创建数据库及表格
    conn = sqlite3.connect('indexroller_1.db')
    c = conn.cursor()
    c.execute('CREATE TABLE IF NOT EXISTS data_table(ID INT,Code INT, Price REAL,'
              ' Date DATE, Time TIME, KEMA REAL, SEMA REAL, LEMA REAL, DIF REAL,'
              ' xlA REAL, xlB REAL, xlC REAL, IsHold INT, KEMAH REAL,'
              ' PriceH REAL, DEA REAL,BuyToday INT)')

def data_read_from_db():
    conn = sqlite3.connect('indexroller_1.db')
    c = conn.cursor()
    c.execute('SELECT * FROM data_table')
    data = c.fetchall()
    c.close()
    return data  #class:list

def get_latest_db_time():
    conn = sqlite3.connect('indexroller_1.db')
    c = conn.cursor()
    c.execute('SELECT Time FROM data_table WHERE ID=1')
    data = c.fetchall()
    c.close()
    result = data[0][0]
    return result  #class:list

def update_db(cmd_text):
    #print(cmd_text)
    conn = sqlite3.connect('indexroller_1.db')
    c = conn.cursor()
    c.execute(cmd_text)
    conn.commit()
    c.close()
    conn.close()

def clear_database():
    conn = sqlite3.connect('indexroller_1.db')
    c = conn.cursor()
    for i in range(1,198 +1):
        cmd = 'DELETE FROM data_table WHERE ID=' + str(i)
        #print(cmd)
        c.execute(cmd)
    conn.commit()
    c.close()
    conn.close()

def data_insert(data_dict):
    conn = sqlite3.connect('indexroller_1.db')
    c = conn.cursor()
    cmd_col = 'ID, Code, Price, Date, Time, KEMA, SEMA, LEMA, DIF,xlA, xlB, xlC, IsHold, KEMAH, PriceH, DEA,BuyToday'
    #command_text = 'INSERT INTO data_table VALUES(' + string_510050 + ')'
    cmd_text = 'INSERT INTO data_table (ID,Code,Price,Date,Time,KEMA,SEMA,LEMA,DIF,xlA,xlB,xlC,IsHold,KEMAH,PriceH,DEA,BuyToday) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)'  # TBD
    #print(cmd_text)
    data_dict_510050 = data_dict_sample
    ID = data_dict.get('ID')  # 0
    Code = data_dict.get('Code')  # 1
    Price = data_dict.get('Price')  # 2
    Date = data_dict.get('Date')  # 3
    Time = data_dict.get('Time')  # 4
    KEMA = data_dict.get('KEMA')  # 5
    SEMA = data_dict.get('SEMA')  # 6
    LEMA = data_dict.get('LEMA')  # 7
    DIF = data_dict.get('DIF')  # 8
    xlA = data_dict.get('xlA')  # 9
    xlB = data_dict.get('xlB')  # 10
    xlC = data_dict.get('xlC')  # 11
    IsHold = data_dict.get('IsHold')  # 12
    KEMAH = data_dict.get('KEMAH')  # 13
    PriceH = data_dict.get('PriceH')  # 14
    DEA = data_dict.get('DEA')  # 15
    BuyToday = data_dict.get('BuyToday')  # 16
    c.execute(cmd_text,(ID,Code,Price,Date,Time,KEMA,SEMA,LEMA,DIF,xlA,xlB,xlC,IsHold,KEMAH,PriceH,DEA,BuyToday))  # TBD
    conn.commit()
    c.close()
    conn.close()


creat_table()
#data_insert(data_dict_sample)
#data_read_from_db()


stock_code_list = [510050,159915,150023]
def get_sina_stock_price(stock_code_list):  # http://hq.sinajs.cn/list=sh510050,sz159915,sz150023
    stock_code_string = ''
    for i in range(0,len(stock_code_list)):
        if (i == 0):
            if str(stock_code_list[i]).startswith(('5', '6', '9')):
                stock_code_string = 'sh' + str(stock_code_list[i])
            else:
                stock_code_string = 'sz' + str(stock_code_list[i])
        else:
            if str(stock_code_list[i]).startswith(('5', '6', '9')):
                stock_code_string =stock_code_string + ',sh' + stock_code_list[i]
            else:
                stock_code_string =stock_code_string + ',sz' + str(stock_code_list[i])
    url = 'http://hq.sinajs.cn/list=' + stock_code_string
    try:
        response = urllib.request.urlopen(url)
        content = response.read()
        content_string = bytes.decode(content, 'GBK')
        content_list = content_string.split(';')  # class:list
        stock_dict_list = [0] * len(stock_code_list)
        #print(len(content_string))
    except:
        content_string = ''
    if (len(content_string)>500):
        for i in range(0, len(stock_code_list)):
            each_index_list = content_list[i].split(',')
            # print('each_index_list: ', each_index_list)
            # print('each_index_list length: ', len(each_index_list))
            stock_dict = dict(
                code=int(stock_code_list[i]),  # each_index_list[0],
                open=float(each_index_list[1]),
                last=float(each_index_list[2]),
                now=float(each_index_list[3]),
                high=float(each_index_list[4]),
                low=float(each_index_list[5]),
                buy=float(each_index_list[6]),
                sell=float(each_index_list[7]),
                volume=int(each_index_list[8]),
                amount=float(each_index_list[9]),
                buy1_volume=int(each_index_list[10]),
                buy1=float(each_index_list[11]),
                buy2_volume=int(each_index_list[12]),
                buy2=float(each_index_list[13]),
                buy3_volume=int(each_index_list[14]),
                buy3=float(each_index_list[15]),
                buy4_volume=int(each_index_list[16]),
                buy4=float(each_index_list[17]),
                buy5_volume=int(each_index_list[18]),
                buy5=float(each_index_list[19]),
                sell1_volume=int(each_index_list[20]),
                sell1=float(each_index_list[21]),
                sell2_volume=int(each_index_list[22]),
                sell2=float(each_index_list[23]),
                sell3_volume=int(each_index_list[24]),
                sell3=float(each_index_list[25]),
                sell4_volume=int(each_index_list[26]),
                sell4=float(each_index_list[27]),
                sell5_volume=int(each_index_list[28]),
                sell5=float(each_index_list[29]),
                date=str(each_index_list[30]),
                time=str(each_index_list[31])
            )
            stock_dict_list[i] = stock_dict
        return_dict = dict(
            code510050=stock_dict_list[0],
            code159915=stock_dict_list[1],
            code150023=stock_dict_list[2],
    )
    if (len(content_string) > 500):
        result = return_dict
    else:
        result = ''  # 返回值：空值，表示网络异常
    return result


#获取股票数据:现价、卖价、买价
def get_stock_price(stock_code,price_type):
    #quotation=easyquotation.use('lf') # ['leverfun', 'lf']#class:dict
    #price_now=quotation.stocks(str(stock_code)).get(str(stock_code)).get('now')
    #price_sell=quotation.stocks(str(stock_code)).get(str(stock_code)).get('sell')
    #price_buy=quotation.stocks(str(stock_code)).get(str(stock_code)).get('buy')
    sinaq = get_sina_stock_price(stock_code_list)
    stock_code_str = 'code' + str(stock_code)
    price_now = sinaq.get(stock_code_str).get('now')
    price_sell = sinaq.get(stock_code_str).get('sell')
    price_buy = sinaq.get(stock_code_str).get('buy')
    if price_type == 'now':
        return price_now
    elif price_type == 'sell':
        return price_sell
    else:
        return price_buy
def get_price_now(stock_code):  # class:float浮点类型
    price = get_stock_price(stock_code, 'now')
    return price
    #print(price)
def get_price_sell(stock_code):  # class:float浮点类型
    price = get_stock_price(stock_code, 'sell')
    return price
    #print(price)
def get_price_buy(stock_code):  # class:float浮点类型
    price = get_stock_price(stock_code, 'buy')
    return price
    #print(price)


def get_stock_price_sina_all():
    q = easyquotation.use("sina")
    q_price = q.all
    price_now_510050 = q_price.get('510050').get('now')
    price_sell_510050 = q_price.get('510050').get('sell')
    price_buy_510050 = q_price.get('510050').get('buy')
    price_date_510050 = q_price.get('510050').get('date')
    price_time_159915 = q_price.get('159915').get('time')
    price_now_159915 = q_price.get('159915').get('now')
    price_sell_159915 = q_price.get('159915').get('sell')
    price_buy_159915 = q_price.get('159915').get('buy')
    price_date_159915 = q_price.get('159915').get('date')
    price_time_159915 = q_price.get('159915').get('time')
    price_now_150023 = q_price.get('150023').get('now')
    price_sell_150023 = q_price.get('150023').get('sell')
    price_buy_150023 = q_price.get('150023').get('buy')
    price_date_150023 = q_price.get('150023').get('date')
    price_time_150023 = q_price.get('150023').get('time')
    print(price_now_510050)


#华泰证券交易
def htStockBuy(StockCode,StockPrice,StockAmount):  # 买入
    user=easytrader.use('ht')  # 设置账户
    user.prepare('ht.json')  # 自动登录
    user.buy(StockCode,price=StockPrice,amount=StockAmount)  # 买入


# 大程序，卖出非计划持仓股票，买入计划持仓股票
def ht_hold_stock(stock_code_buy):#卖一价买入510050，立即成交.0的话则只卖出不买入
    print('进入华泰股票操作程序')
    user =easytrader.use('ht')#设置账户
    user.prepare('ht.json')#自动登录
    position = user.position  # class:list一个股票持仓，list含有一个元素，两个股票持仓，list含有两个元素，每个元素都是dict类型

    # 查询股票持仓，确认可卖出的股票代码、数量
    def ht_get_hold():
        print('开始查询账户持仓情况')
        # 查询股票持仓，确认可卖出的股票代码、数量
        hold_index_qty = len(position)  # 获取持仓指数数量
        hold_stock_code_1=0
        hold_stock_amount_1=0
        hold_stock_code_2=0
        hold_stock_amount_2=0
        hold_stock_code_3=0
        hold_stock_amount_3=0
        if (hold_index_qty == 1):
            hold_stock_code_1 = position[0].get('stock_code')  # 获取持仓股票代码0
            hold_stock_amount_1 = position[0].get('current_amount')  # 获取持仓股票持股数0
        elif (hold_index_qty == 2):
            hold_stock_code_1 = position[0].get('stock_code')  # 获取持仓股票代码0
            hold_stock_amount_1 = position[0].get('current_amount')  # 获取持仓股票持股数0
            hold_stock_code_2 = position[1].get('stock_code')
            hold_stock_amount_2 = position[1].get('current_amount')
        elif (hold_index_qty == 3):
            hold_stock_code_1 = position[0].get('stock_code')  # 获取持仓股票代码0
            hold_stock_amount_1 = position[0].get('current_amount')  # 获取持仓股票持股数0
            hold_stock_code_2 = position[1].get('stock_code')
            hold_stock_amount_2 = position[1].get('current_amount')
            hold_stock_code_3 = position[2].get('stock_code')
            hold_stock_amount_3 = position[2].get('current_amount')
        #print('hold_index_qty: ',hold_index_qty)
        #print(position[0].get('stock_code'))
        #print(position[1])
        #print(hold_stock_code_1)
        #print(hold_stock_amount_1)
        #print(hold_stock_code_2)
        #print(hold_stock_amount_2)
        #print(hold_stock_code_3)
        #print(hold_stock_amount_3)
        hold_stock_list = [int(hold_stock_code_1), int(hold_stock_amount_1), int(hold_stock_code_2), int(hold_stock_amount_2), int(hold_stock_code_3), int(hold_stock_amount_3)]
        hold_stock_dic = dict(amount511880=0,amount510050=0,amount159915=0,amount150023=0)
        #print('hold_stock_list', hold_stock_list)
        #print('511880 index: ', hold_stock_list.index(511880))
        if 511880 in hold_stock_list:
            hold_stock_dic['amount511880'] = hold_stock_list[hold_stock_list.index(511880)+1]
        if 510050 in hold_stock_list:
            hold_stock_dic['amount510050'] = hold_stock_list[hold_stock_list.index(510050)+1]
        if 159915 in hold_stock_list:
            hold_stock_dic['amount159915'] = hold_stock_list[hold_stock_list.index(159915)+1]
        if 150023 in hold_stock_list:
            hold_stock_dic['amount150023'] = hold_stock_list[hold_stock_list.index(150023)+1]
        result = hold_stock_dic
        print('账户持仓情况如下：\n')
        print(result)
        return result

    # 先卖出持仓股票
    def sell_hold_stocks(stock_code_buy):
        print('开始卖出非计划持仓股票，计划持仓股票代码：', stock_code_buy)
        hold_stock_dict = ht_get_hold()
        if (stock_code_buy == 510050):
            if (hold_stock_dict.get('amount159915') != 0):
                buy_price = get_price_buy(159915)
                user.sell(str(159915),price=buy_price,amount=hold_stock_dict.get('amount159915'))  # 卖出
                print('卖出持仓股票：159915，计划卖出价格：',buy_price,'，计划卖出数量：',hold_stock_dict.get('amount159915'))
                time.sleep(15)  #暂停进程，给卖出时间
            else:
                print('159915持仓为零')
            if (hold_stock_dict.get('amount150023') != 0):
                buy_price = get_price_buy(150023)
                user.sell(str(150023),price=buy_price,amount=hold_stock_dict.get('amount150023'))  # 卖出
                print('卖出持仓股票：150023，计划卖出价格：',buy_price,'，计划卖出数量：',hold_stock_dict.get('amount150023'))
                time.sleep(15)  #暂停进程，给卖出时间
            else:
                print('150023持仓为零')
        elif (stock_code_buy==159915):
            if (hold_stock_dict.get('amount510050') != 0):
                buy_price = get_price_buy(510050)
                user.sell(str(510050),price=buy_price,amount=hold_stock_dict.get('amount510050'))  # 卖出
                print('卖出持仓股票：510050，计划卖出价格：',buy_price,'，计划卖出数量：',hold_stock_dict.get('amount510050'))
                time.sleep(15)  #暂停进程，给卖出时间
            else:
                print('510050持仓为零')
            if (hold_stock_dict.get('amount150023') != 0):
                buy_price = get_price_buy(150023)
                user.sell(str(150023),price=buy_price,amount=hold_stock_dict.get('amount150023'))  # 卖出
                print('卖出持仓股票：150023，计划卖出价格：',buy_price,'，计划卖出数量：',hold_stock_dict.get('amount150023'))
                time.sleep(15)  #暂停进程，给卖出时间
            else:
                print('150023持仓为零')
        elif (stock_code_buy==150023):
            if (hold_stock_dict.get('amount510050') != 0):
                buy_price = get_price_buy(510050)
                user.sell(str(510050),price=buy_price,amount=hold_stock_dict.get('amount510050'))  # 卖出
                print('卖出持仓股票：510050，计划卖出价格：',buy_price,'，计划卖出数量：',hold_stock_dict.get('amount510050'))
                time.sleep(15)  #暂停进程，给卖出时间
            else:
                print('510050持仓为零')
            if (hold_stock_dict.get('amount159915') != 0):
                buy_price = get_price_buy(159915)
                user.sell(str(159915),price=buy_price,amount=hold_stock_dict.get('amount159915'))  # 卖出
                print('卖出持仓股票：159915，计划卖出价格：',buy_price,'，计划卖出数量：',hold_stock_dict.get('amount159915'))
                time.sleep(15)  #暂停进程，给卖出时间
            else:
                print('159915持仓为零')
        elif (stock_code_buy==0):
            if (hold_stock_dict.get('amount510050') != 0):
                buy_price = get_price_buy(510050)
                user.sell(str(510050),price=buy_price,amount=hold_stock_dict.get('amount510050'))  # 卖出
                print('卖出持仓股票：510050，计划卖出价格：',buy_price,'，计划卖出数量：',hold_stock_dict.get('amount510050'))
                time.sleep(15)  #暂停进程，给卖出时间
            if (hold_stock_dict.get('amount159915') != 0):
                buy_price = get_price_buy(159915)
                user.sell(str(159915),price=buy_price,amount=hold_stock_dict.get('amount159915'))  # 卖出
                print('卖出持仓股票：159915，计划卖出价格：',buy_price,'，计划卖出数量：',hold_stock_dict.get('amount159915'))
                time.sleep(15)  #暂停进程，给卖出时间
            if (hold_stock_dict.get('amount150023') != 0):
                buy_price = get_price_buy(150023)
                user.sell(str(150023),price=buy_price,amount=hold_stock_dict.get('amount150023'))  # 卖出
                print('卖出持仓股票：150023，计划卖出价格：',buy_price,'，计划卖出数量：',hold_stock_dict.get('amount150023'))
                time.sleep(15)  #暂停进程，给卖出时间
    sell_hold_stocks(stock_code_buy)

    # 获取资金状况
    def get_enable_balance():  # 如何保证重新查询时，是最新的数据？？？？？？？？？？？？？？？？？？？？？？？？？？？？？？？？？？？？？？？？？？？？？？？？？？？
        balance = user.balance
        enable_balance = balance[0].get('enable_balance')  # 可用余额
        asset_balance = balance[0].get('asset_balance')  # 资产总额
        result = enable_balance
        return result
    enable_balance = get_enable_balance()
    if (enable_balance > 1000):  # 持仓未完全卖出，再执行卖出程序卖出
        sell_hold_stocks(stock_code_buy)  # 再次卖出持仓股票


    # 买入目标股票
    def buy_aim_stock(stock_code_buy):
        sell_price = get_price_sell(stock_code_buy)
        cash = get_enable_balance()  # 查询可交易的现金
        print('查询可交易现金：',cash)
        buy_amount = cash // (sell_price * 100.035)  # 取整除法，考虑手续费
        # buy_amount = buy_amount_0//1  # 取整除法
        if (buy_amount > 0):
            user.buy(str(stock_code_buy), price=sell_price, amount=buy_amount * 100)  # 买入
            print('买入计划持仓股票：', stock_code_buy, '，计划买入价格：', sell_price, '，计划买入数量：', buy_amount * 100)
    if (stock_code_buy==0):
        print('收到清仓指令“stock_code_buy=0”，已执行清仓，不买入')
    else:
        buy_aim_stock(stock_code_buy)
        time.sleep(15)  #暂停进程，给买入时间
        cash_2 = get_enable_balance()  # 再次查询资产情况
        print('再次查询,判断是否再次买入，目前可交易现金：', cash_2)
        if (cash_2>1000):
            print('进行再次交易')
            buy_aim_stock(stock_code_buy)  # 再次买入
            time.sleep(15)  # 暂停进程，给买入时间


def ht_hold_510050():
    ht_hold_stock(510050)
def ht_hold_159915():
    ht_hold_stock(159915)
def ht_hold_150023():
    ht_hold_stock(150023)


def htStockSell():#卖出
    user =easytrader.use('ht')#设置账户
    user.prepare('ht.json')#自动登录
    user.sell('510050',price=123.000,amount=100)  # 卖出


def htgetBalance():  # 获取今日委托--》撤单--》获取持仓--》获取资金状况
    user =easytrader.use('ht')  # 设置账户
    user.prepare('ht.json')  # 自动登录
    balance=user.balance  # 获取资金状况
    print(balance)
    #user.entrust  # 获取今日委托单
    # #user.cancel_entrust()#撤单


def dea_cal( PriceNow, KEMALst, SEMALst, LEMALst, DEALst,  xlALst, xlBLst, IsHoldLst, KEMAHLst, PriceHLst, BuyTodayLst, DateLst, DateNow):
    #  计算KEMA\SEMA\LEMA\DIF
    #print('PriceNow=',PriceNow)
    #print('KEMALst=',KEMALst)
    #print('SEMALst=',SEMALst)
    #print('LEMALst=',LEMALst)
    #print('DEALst=',DEALst)
    #print('xlA=',xlALst)
    #print('xlA=', xlBLst)
    #print('IsHoldLst=',IsHoldLst)
    #print('KEMAHLst=',KEMAHLst)
    #print('PriceHLst=',PriceHLst)
    #print('BuyTodayLst=',BuyTodayLst)
    #print('DateLst=',DateLst)
    #print('DateNow=',DateNow)
    KEMAN = 16.0
    SEMAN = 64.0
    LEMAN = 64.0
    KEMA = KEMALst  # 昨日数据
    PTD = PriceNow  # 今日数据
    KEMA = KEMA * (KEMAN - 1) / (KEMAN + 1) + PTD * 2 / (KEMAN + 1)
    SEMA = SEMALst
    PTD = PriceNow
    SEMA = SEMA * (SEMAN - 1) / (SEMAN + 1) + PTD * 2 / (SEMAN + 1)
    LEMA = LEMALst
    PTD = PriceNow
    LEMA = LEMA * (LEMAN - 1) / (LEMAN + 1) + PTD * 2 / (LEMAN + 1)
    DIF = SEMA - LEMA
    # 计算前1、2、3天短期EMA斜率XLA\XLB\XLC
    xlA = (SEMA - SEMALst) / SEMALst  # 今日斜率
    xlB = xlALst
    xlC = xlBLst  #前三天SEMA斜率
    # 计算xlA的移动EMA均值
    DEAN = 7.0
    DEA = DEALst  #SEMA斜率7日指数平滑异同均值
    PTD = xlA
    DEA = DEA * (DEAN - 1) / (DEAN + 1) + PTD * 2 / (DEAN + 1)
    # 计算PriceH、KEMAH
    if (IsHoldLst == 0):  # 前交易日空仓
        KEMAH = KEMA
        PriceH = PriceNow
    else:  # 前交易日持仓
        KEMAH = KEMAHLst
        if (KEMA > KEMAHLst):
            KEMAH = KEMA
        PriceH = PriceHLst
        if (PriceNow > PriceH):
            PriceH = PriceNow
    # 计算今日交易额度
    if (DateLst != DateNow):
        BuyToday = 1
    else:
        BuyToday = BuyTodayLst
    final_data_dic = {'KEMA': KEMA,
                      'SEMA': SEMA,
                      'LEMA': LEMA,
                      'DIF': DIF,
                      'DEA': DEA,
                      'xlA': xlA,
                      'xlB': xlB,
                      'xlC': xlC,
                      'KEMAH': KEMAH,
                      'PriceH': PriceH,
                      'BuyToday':BuyToday}
    return final_data_dic


def get_new_db_data(db_data_old,network_data):  # 输入旧的数据库数据+网络数据=新的待写入数据库的数据:list+list
    #db_data_new = db_data_old  # class:tuple元组数据类型不可以修改
    #print('342传入函数的旧数据库数据如下：')  # tuple和list非常类似，但是tuple一旦初始化就不能修改
    #print(db_data_old)
    #print(len(db_data_old))
    #print(type(db_data_old))
    #print(type(db_data_old[0]))
    # (1, 510050, 0.123, '2016-03-22', '11:12:05', 0.123, 0.123, 0.123, 0.123, 0.123, 0.123, 0.123, 0, 0.123, 0.123, 0.123, 1)
    def cal_sina_data(db_data_old_row1, sina_data):
        index_data = IndexData()
        #print('本组待处理网络数据如下: ',sina_data)
        index_data.Code = sina_data[0]
        if index_data.Code == 510050:
            index_data.ID = 1
        elif index_data.Code == 159915:
            index_data.ID = 2
        elif index_data.Code == 150023:
            index_data.ID = 3
        index_data.Price = sina_data[1]
        index_data.Date = sina_data[2]
        index_data.Time = sina_data[3]
        #print('本组待处理数据库第一组数据如下：',db_data_old_row1)
        dea_data_new = dea_cal(sina_data[1], db_data_old_row1[5], db_data_old_row1[6], db_data_old_row1[7],db_data_old_row1[15], db_data_old_row1[9], db_data_old_row1[10], db_data_old_row1[12],db_data_old_row1[13], db_data_old_row1[14], db_data_old_row1[16], db_data_old_row1[3],sina_data[2])
        index_data.KEMA = dea_data_new.get('KEMA')
        index_data.SEMA = dea_data_new.get('SEMA')
        index_data.LEMA = dea_data_new.get('LEMA')
        index_data.DIF = dea_data_new.get('DIF')
        index_data.xlA = dea_data_new.get('xlA')
        index_data.xlB = dea_data_new.get('xlB')
        index_data.IsHold = 0  # 暂设置默认值
        index_data.xlC = dea_data_new.get('xlC')
        index_data.KEMAH = dea_data_new.get('KEMAH')
        index_data.PriceH = dea_data_new.get('PriceH')
        index_data.DEA = dea_data_new.get('DEA')
        index_data.BuyToday = dea_data_new.get('BuyToday')
        index_data_tuple =(index_data.ID,index_data.Code,index_data.Price,index_data.Date,index_data.Time,index_data.KEMA,index_data.SEMA,index_data.LEMA,index_data.DIF,index_data.xlA,index_data.xlB,index_data.xlC,index_data.IsHold,index_data.KEMAH,index_data.PriceH,index_data.DEA,index_data.BuyToday)
        #print('373处理后网络数据如下：',index_data_tuple)
        return index_data_tuple
    #db_data_new[0] = network_data[0]
    #print('385待处理网络数据如下: ',network_data)
    db_data_new = [0]*198  # 空列表
    for i in range( 0,2 + 1 ):  # 0.1.2
        #print('401本组待传入函数处理的旧数据库数据如下：',db_data_old[i])
        #print('402本组待传入函数处理的网络数据如下：',network_data[i])
        #print(i)
        db_data_new[i] = cal_sina_data(db_data_old[i],network_data[i])
        #print('392本组处理完后的数据如下：',db_data_new)
    for i in range( 3,198 + 0 ):  # 3.4.5...197.198
        #print(type(db_data_old))
        #print(type(db_data_old[i-3]))
        #print(db_data_old[i - 3][0])
        if ( i < len(db_data_old) + 3):  # 0-197=198. 198+3=201. i<201.
            #print(i)
            #print(len(db_data_old))
            list_temp = list(db_data_old[i - 3])  # tuple转化为list
            list_temp[0] = i + 1  # 修改原来ID值，从4开始
            tuple_temp = tuple(list_temp)  # list转化为tuple
            #print('Line414 i=',i)
            db_data_new[i] = tuple_temp
            #print(db_data_new)
        else:
            break

    #print(db_data_new)

    return db_data_new  # class:list

def if_time_is_ok(data_time_hm,data_time_ms):
    time_is_ok = False
    #print('hm:',data_time_hm)
    #print('ms:',data_time_ms)
    latest_db_time = get_latest_db_time()
    latest_db_time_hhmm = latest_db_time[0:5]
    #print(latest_db_time)
    #print('506',latest_db_time_hhmm)
    #print(data_time_hm)
    time_is_ok_0 = (data_time_hm != latest_db_time_hhmm)
    time_is_ok_1 = (data_time_hm == '09:00' or data_time_hm == '09:05' or data_time_hm == '09:10' or data_time_hm == '09:15' or data_time_hm == '09:20' or data_time_hm == '09:25' or data_time_hm == '09:30')
    time_is_ok_2 = (data_time_hm == '11:35' or data_time_hm == '13:00' or data_time_hm == '15:05')
    time_is_ok_3 = (data_time_ms=='0:00' or data_time_ms=='0:01' or data_time_ms=='0:02' or data_time_ms=='0:03' or data_time_ms=='0:04' or data_time_ms=='0:05' or data_time_ms=='0:06'
                    or data_time_ms=='0:07' or data_time_ms=='0:08' or data_time_ms=='0:09' or data_time_ms=='0:10' or data_time_ms=='0:11' or data_time_ms=='0:12' or data_time_ms == '0:13'
                    or data_time_ms == '0:14' or data_time_ms == '0:15' or data_time_ms == '0:16' or data_time_ms == '0:17' or data_time_ms == '0:18' or data_time_ms == '0:19')
    time_is_ok_4 = (data_time_ms=='5:00' or data_time_ms=='5:01' or data_time_ms=='5:02' or data_time_ms=='5:03' or data_time_ms=='5:04' or data_time_ms=='5:05' or data_time_ms=='5:06'
                    or data_time_ms=='5:07' or data_time_ms=='5:08' or data_time_ms=='5:09' or data_time_ms=='5:10' or data_time_ms=='5:11' or data_time_ms=='5:12' or data_time_ms == '5:13'
                    or data_time_ms == '5:14' or data_time_ms == '5:15' or data_time_ms == '5:16' or data_time_ms == '5:17' or data_time_ms == '5:18' or data_time_ms == '5:19')
    # TODO CHANGE TIME SETTINGS
    #time_is_ok_0 = True # 强制采集更多数据
    #time_is_ok_3 = True  # 强制采集更多数据
    #time_is_ok_4 = True  # 强制采集更多数据
    time_is_ok = (time_is_ok_0==True and time_is_ok_1==False and time_is_ok_2==False and (time_is_ok_3==True or time_is_ok_4==True))
    #print('time_is_ok_1 hm: ',data_time_hm)
    #print('time_is_ok_2 hm: ',time_is_ok_2)
    #print('time_is_ok_3 ms: ',time_is_ok_3)
    #print('time_is_ok_4 ms: ',time_is_ok_4)
    #print('time_is_ok: ',time_is_ok)
    return time_is_ok

def get_db_network_data():
    sinaq = get_sina_stock_price(stock_code_list)
    if (sinaq == ''):
        result_dict = ''
    else:
        price_now_510050 = sinaq.get('code510050').get('now')
        price_sell_510050 = sinaq.get('code510050').get('sell')
        price_buy_510050 = sinaq.get('code510050').get('buy')
        price_date_510050 = sinaq.get('code510050').get('date')
        price_time_510050 = sinaq.get('code510050').get('time')
        price_now_159915 = sinaq.get('code159915').get('now')
        price_sell_159915 = sinaq.get('code159915').get('sell')
        price_buy_159915 = sinaq.get('code159915').get('buy')
        price_date_159915 = sinaq.get('code159915').get('date')
        price_time_159915 = sinaq.get('code159915').get('time')
        price_now_150023 = sinaq.get('code150023').get('now')
        price_sell_150023 = sinaq.get('code150023').get('sell')
        price_buy_150023 = sinaq.get('code150023').get('buy')
        price_date_150023 = sinaq.get('code150023').get('date')
        price_time_150023 = sinaq.get('code150023').get('time')
        if (price_now_510050 == 0) or (price_now_159915 == 0 ) or (price_now_150023 == 0):
            result_dict = ''
        else:
            result_dict= {'510050': {'now': price_now_510050, 'date': price_date_510050, 'time': price_time_510050},
                           '159915': {'now': price_now_159915, 'date': price_date_159915, 'time': price_time_159915},
                           '150023': {'now': price_now_150023, 'date': price_date_150023, 'time': price_time_150023}}
    result = result_dict
    return result

def index_roller_auto():
    print('Line706 自动模式启动')
    loop_cal = 1  #计算累计循环次数
    while ( True ):
        unix = time.time()
        system_date_ymdhms_string = str(datetime.datetime.fromtimestamp(unix).strftime('%Y-%m-%d %H:%M:%S'))  # 获取系统时间
        system_date_ymd_string = str(datetime.datetime.fromtimestamp(unix).strftime('%Y-%m-%d'))  # 获取系统时间日期
        system_time_hms_string = str(datetime.datetime.fromtimestamp(unix).strftime('%H:%M:%S'))  # 获取系统时间分钟秒时间
        # 获取网络数据，间隔2秒
        #TODO 修改循环时间
        time_loop = 3
        time.sleep(time_loop)  # 间隔2秒执行
        #print('Line696 进入While循环次数：', loop_cal)
        loop_cal = loop_cal + 1
        sina_data_dict = get_db_network_data()  # 获取网络数据，返回list格式
        if (sina_data_dict == ''):
            print(system_date_ymdhms_string, ' Network error')
        else:  # 网络正常，执行程序
            price_now_510050 = sina_data_dict.get('510050').get('now')
            price_date_510050 = sina_data_dict.get('510050').get('date')
            price_time_510050 = sina_data_dict.get('510050').get('time')
            price_now_159915 = sina_data_dict.get('159915').get('now')
            price_date_159915 = sina_data_dict.get('159915').get('date')
            price_time_159915 = sina_data_dict.get('159915').get('time')
            price_now_150023 = sina_data_dict.get('150023').get('now')
            price_date_150023 = sina_data_dict.get('150023').get('date')
            price_time_150023 = sina_data_dict.get('150023').get('time')
            time_netwowk_hm = price_time_510050[0:5]
            time_netwowk_ms = price_time_510050[4:8]
            network_list = [(510050, price_now_510050, price_date_510050, price_time_510050),
                            (159915, price_now_159915, price_date_159915, price_time_159915),
                            (150023, price_now_150023, price_date_150023, price_time_150023)]
            # 判断数据时间是否可录入
            print('Line568 ',system_date_ymdhms_string, ' 网络数据如下', network_list)  # 分钟
            time_isOK = False
            time_isOK = if_time_is_ok(time_netwowk_hm,time_netwowk_ms)
            #print('time_isOK = ',time_isOK)
            if (time_isOK == True ):  # 网络时间OK，数据可以考虑录入# 获取数据库数据
                #print('开始读取数据库数据')
                db_list_old = data_read_from_db()  # class:list
                #print('Line592 网络数据如下:',network_list)
                db_list_new = get_new_db_data(db_list_old,network_list)  # 新的数据，可以写入数据库
                clear_database()  # 清空数据库
                print('Line596 数据库清空完成')
                print('Line597 开始写入新数据到数据库')
                for i in range(0,198):
                    if (db_list_new[i] != 0):
                        list_dic_key = ['ID', 'Code', 'Price', 'Date', 'Time', 'KEMA', 'SEMA', 'LEMA', 'DIF', 'xlA', 'xlB', 'xlC', 'IsHold', 'KEMAH', 'PriceH', 'DEA','BuyToday']
                        list_dic_value = list(db_list_new[i])
                        list_dic = dict(zip(list_dic_key,list_dic_value))
                        data_insert(list_dic)
                    else:
                        break
                print('Line601 新数据写入数据库完成')
                # 是否进行交易
                print('Line604 开始判断是否交易')
                def get_new_dict(i):  # 获取指定ID在数据库中的数据
                    list_dic_key = ['ID', 'Code', 'Price', 'Date', 'Time', 'KEMA', 'SEMA', 'LEMA', 'DIF', 'xlA', 'xlB', 'xlC', 'IsHold', 'KEMAH', 'PriceH', 'DEA','BuyToday']
                    list_dic_value = list(db_list_new[i])
                    list_dic = dict(zip(list_dic_key,list_dic_value))
                    return list_dic
                dic_510050 = get_new_dict(0)
                dic_159915 = get_new_dict(1)
                dic_150023 = get_new_dict(2)
                dic_510050_lst = get_new_dict(3)
                dic_159915_lst = get_new_dict(4)
                dic_150023_lst = get_new_dict(5)
                buy_today = dic_510050.get('BuyToday')
                def get_dea_high_now():  # 计算DEA今日斜率最高的指数
                        DEAH = 0
                        DEAH_CODE = 0
                        DEAH_ID = 0
                        DEA_510050 = dic_510050.get('DEA')
                        DEA_159915 = dic_159915.get('DEA')
                        DEA_150023 = dic_150023.get('DEA')
                        if (DEA_510050 >= max(DEA_159915,DEA_150023)):
                            DEAH = DEA_510050
                            DEAH_CODE = 510050
                            DEAH_ID = 1
                        elif (DEA_159915 >= DEA_150023):
                            DEAH = DEA_159915
                            DEAH_CODE = 159915
                            DEAH_ID = 2
                        else:
                            DEAH = DEA_150023
                            DEAH_CODE = 150023
                            DEAH_ID = 3
                        result = dict(DEAH=DEAH, DEAH_CODE=DEAH_CODE,DEAH_ID=DEAH_ID)
                        return result
                def get_hold_lst():
                        Hold_DEA_Lst = 0
                        Hold_Code_Lst = 0
                        Hold_ID_Lst = 0
                        if (dic_510050_lst.get('IsHold')==1):
                            Hold_DEA_Lst = dic_510050_lst.get('DEA')
                            Hold_Code_Lst = 510050
                            Hold_ID_Lst = 1
                        elif (dic_159915_lst.get('IsHold')==1):
                            Hold_DEA_Lst = dic_159915_lst.get('DEA')
                            Hold_Code_Lst = 159915
                            Hold_ID_Lst = 2
                        elif (dic_150023_lst.get('IsHold')==1):
                            Hold_DEA_Lst = dic_150023_lst.get('DEA')
                            Hold_Code_Lst = 150023
                            Hold_ID_Lst = 3
                        else:
                            Hold_DEA_Lst=0
                            Hold_Code_Lst=0
                            Hold_ID_Lst = 0
                        result = dict(HOLD_DEA=Hold_DEA_Lst, HOLD_CODE=Hold_Code_Lst, HOLD_ID=Hold_ID_Lst)
                        return result
                get_dea_high_n = get_dea_high_now()
                DEAH_NOW = get_dea_high_n.get('DEAH')
                DEAH_CODE_NOW = int(get_dea_high_n.get('DEAH_CODE'))
                DEAH_ID_NOW = int(get_dea_high_n.get('DEAH_ID'))
                get_hold = get_hold_lst()
                Hold_DEA_Lst = get_hold.get('HOLD_DEA')
                Hold_Code_Lst = int(get_hold.get('HOLD_CODE'))
                Hold_ID_Lst = int(get_hold.get('HOLD_ID'))
                if (buy_today==1):
                    print('Line618 交易额度有余，可以进行交易')
                    if (Hold_Code_Lst==0):  # 昨日空仓
                        if (DEAH_NOW < 0.000006):
                            print('保持空仓')
                        else:
                            print('建仓，持有指数：',DEAH_CODE_NOW)
                            cmd_text = 'UPDATE data_table SET IsHold = 1 WHERE ID=' + str(DEAH_ID_NOW)
                            update_db(cmd_text)
                            cmd_text = 'UPDATE data_table SET BuyToday = 0 WHERE ID=1'
                            update_db(cmd_text)
                            cmd_text = 'UPDATE data_table SET BuyToday = 0 WHERE ID=2'
                            update_db(cmd_text)
                            cmd_text = 'UPDATE data_table SET BuyToday = 0 WHERE ID=3'
                            update_db(cmd_text)
                            ht_hold_stock(DEAH_CODE_NOW)
                    else:  # 昨日持仓
                        if (DEAH_NOW < 0.000006):  # 空仓
                            print('空仓,卖出持有指数')
                            cmd_text = 'UPDATE data_table SET BuyToday = 1 WHERE ID=1'
                            update_db(cmd_text)
                            cmd_text = 'UPDATE data_table SET BuyToday = 1 WHERE ID=2'
                            update_db(cmd_text)
                            cmd_text = 'UPDATE data_table SET BuyToday = 1 WHERE ID=3'
                            update_db(cmd_text)
                            ht_hold_stock(0)
                        else:
                            if (DEAH_NOW - Hold_DEA_Lst > 0.00015):
                                print('换仓至指数：', DEAH_CODE_NOW)
                                cmd_text = 'UPDATE data_table SET IsHold = 1 WHERE ID=' + str(DEAH_ID_NOW)
                                update_db(cmd_text)
                                cmd_text = 'UPDATE data_table SET BuyToday = 0 WHERE ID=1'
                                update_db(cmd_text)
                                cmd_text = 'UPDATE data_table SET BuyToday = 0 WHERE ID=2'
                                update_db(cmd_text)
                                cmd_text = 'UPDATE data_table SET BuyToday = 0 WHERE ID=3'
                                update_db(cmd_text)
                                ht_hold_stock(DEAH_CODE_NOW)
                            else:
                                print('未达到切换标准，继续持有指数：', Hold_Code_Lst)
                                cmd_text = 'UPDATE data_table SET IsHold = 1 WHERE ID=' + str(Hold_ID_Lst)
                                update_db(cmd_text)
                else:
                    print('DEAH=',DEAH_NOW,'DEAH Code=',DEAH_CODE_NOW,'DEAH ID=',DEAH_ID_NOW)
                    print('Hold DEA=',Hold_DEA_Lst,'Hold Code=',Hold_Code_Lst,'Hold ID=',Hold_ID_Lst)
                    print('交易额度不足，今日不交易，继续持有指数：', Hold_Code_Lst)
                    cmd_text = 'UPDATE data_table SET IsHold = 1 WHERE ID=' + str(Hold_ID_Lst)
                    update_db(cmd_text)


#============================================================================================================
##index_roller_auto()

def main():
    print('进入主程序')
    index_roller_auto()

if __name__ == '__main__':
    main()


