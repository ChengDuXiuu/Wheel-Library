from datetime import datetime
import threading
import requests
import time
from apscheduler.schedulers.blocking import BlockingScheduler
from timeCron import cron
from jpushEx import jpushToSanXing

def global_variable_init():
    global id_set
    id_set=set()#存放新库ID


def get_data_list(*args):#话题，语言
    baseUrl = 'https://api.github.com/search/repositories?q='
    # param='topic:'+topic+'+language:'+language+'+created:'+str(datetime.now()).split()[0]
    param = 'topic:' + args[0] + '+language:' + args[1] + '+created:2018-02-08'
    fullUrl = baseUrl + param
    print(fullUrl)

    # 创建互斥锁,默认不上锁
    mutex = threading.Lock()

    #获取数据
    # while True:
    try:
        response=requests.get(fullUrl,timeout=7)
    except Exception as e:
        print(e)
    else:
        if response.status_code==200 :
            datas=response.json()['items']
            if datas :
                print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                mutex.acquire()  # 上锁
                for data in datas:
                    print("获取到一条数据》》》",data['id'])
                    if data['id'] not in id_set:
                        print("********************************不存在************************************8")
                        id_set.add(data['id'])
                        print('name>> ',data['name'],'描述>> ',data['description'])
                        if data['name'] ==None:
                            data['name']=""
                        if data['description']==None:
                            data['description']=''
                        jpushToSanXing.sent_message(data['name']+"  描述：  "+data['description'])
                mutex.release()  # 解锁
        else:
            print("请求失败！！！")


if __name__ == '__main__':
    global_variable_init()

    cron.execute(get_data_list,'crawler','python')

    # 模拟主进程持续运行
    try:
        while True:
            time.sleep(2)
            print('sleep')
    except(KeyboardInterrupt, SystemExit):
        print('Exit The Job!')
    # execute(hello())