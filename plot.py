# encoding:utf-8
__author__ = 'jxcjean'

import matplotlib.pyplot as plt
import numpy as np
import sqlite3
import easyquotation
import os

#x = np.arrange(0, 198, 1)
y = []
z = []
t = []

# 获取昨日收盘价
def get_close_price():
    quotation = easyquotation.use('lf')  # ['leverfun', 'lf']
    qq = quotation.stocks(['510050', '159915', '150023'])
    close_510050 = qq.get('510050').get('close')
    close_159915 = qq.get('159915').get('close')
    close_150023 = qq.get('150023').get('close')
    result_list = [close_510050, close_159915, close_150023]
    return result_list


def data_read_from_db():
    close_list = get_close_price()
    #print(close_list)
    close_510050 = close_list[0]
    close_159915 = close_list[1]
    close_150023 = close_list[2]
    price_510050 = []
    date_510050 = []
    price_159915 = []
    date_159915 = []
    price_150023 = []
    date_150023 = []
    price_open = 1.0
    price_now = 1.0
    conn = sqlite3.connect('indexroller_1.db')
    c = conn.cursor()
    for i in range(1, 66+1):
        cmd_text = 'SELECT Price FROM data_table WHERE ID=' + str(201 - i * 3 - 2)
        c.execute(cmd_text)
        data = c.fetchall()
        price_now = float(data[0][0])/close_510050
        price_510050.append(price_now)
        date_510050.append(i)

        cmd_text = 'SELECT Price FROM data_table WHERE ID=' + str(201 - i * 3 - 1)
        c.execute(cmd_text)
        data = c.fetchall()
        price_now = float(data[0][0]) / close_159915
        price_159915.append(price_now)
        date_159915.append(i)

        cmd_text = 'SELECT Price FROM data_table WHERE ID=' + str(201 - i * 3 - 0)
        c.execute(cmd_text)
        data = c.fetchall()
        price_now = float(data[0][0]) / close_150023
        price_150023.append(price_now)
        date_150023.append(i)

    #print(price_510050)
    #print(price_159915)
    #print(price_150023)
    c.close()

    plt.plot(date_510050, price_510050, label='510050', color='red')
    plt.plot(date_159915, price_159915, label='159915', color='black')
    plt.plot(date_150023, price_150023, label='150023', color='blue')
    ax = plt.gca()

    # 设置两个坐标轴的范围
    plt.xlim(0, 66+1)
    plt.ylim(0.9, 1.1)

    # 开启网格
    plt.grid()

    plt.legend()

    # 保存曲线为图片格式
    #os.unlink('index_plot.png')
    plt.savefig('index_plot.png')
    print('曲线图绘制完毕')
    #result = data[0][0]
    #return data  # class:list  1-198


