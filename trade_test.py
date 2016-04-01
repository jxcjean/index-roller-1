import easytrader
print('进入华泰交易')
user = easytrader.use('ht') # 华泰支持 ['ht', 'HT', '华泰']
user.prepare('ht.json') #或者 yjb.json 或者 yh.json 等配置文件路径
#balance = user.balance
#print(balance)
position = user.position
print(position)