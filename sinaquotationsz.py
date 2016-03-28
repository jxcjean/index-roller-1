import urllib.request
import time


stock_code_list = [510050,159915,150023]


def get_sina_stock_price(stock_code_list):  # http://hq.sinajs.cn/list=sz150181,sz150018
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
        print(len(content_string))
    except:
        content_string = ''
    if (len(content_string)>100):
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
    if (len(content_string) > 100):
        result = return_dict
    else:
        result = ''
    return result

#sina_quotation = get_sina_stock_price(stock_code_list)
#print(sina_quotation)

loop_cal = 0
while (True):
    loop_cal = loop_cal + 1
    print('This try: ',loop_cal)
    time.sleep(5)
    sina_quotation = get_sina_stock_price(stock_code_list)
    print(sina_quotation)

#sina_quotation = get_sina_stock_price(stock_code_list)
#get_sina_stock_price(510050)