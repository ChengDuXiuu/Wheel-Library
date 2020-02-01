from datetime import time

from wxpy import *


if __name__ == '__main__':
   bot=Bot(cache_path=True)

   try:
      # 搜索名称含有 "游否" 的男性深圳好友
      my_friend = bot.friends().search('小可爱', sex=FEMALE, city="山西")[0]
      my_friend.send('hello weChat')
      # 为了不用每次扫码登录，这里使用线程中的Timer函数，每隔一天调用一下程序
      # t = Timer(86400, sent_news)
      # t.start()
   except Exception as e:
      print(e)