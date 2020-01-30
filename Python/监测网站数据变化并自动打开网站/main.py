import time

import requests
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.schedulers.background import BackgroundScheduler
import prettytable as pt
import webbrowser as broswer

tb = pt.PrettyTable()
tb.field_names = ["参数", "说明"]
tb.add_row(["year(int or str)","年，4位数字"])
tb.add_row(["month(int or str)","月（范围1-12）"])
tb.add_row(["day(int or str)", "日（范围1-31）"])
tb.add_row(["week(int or str)", "周（范围1-53）"])
tb.add_row(["day_of_week(int or str)", "周内第几天或者星期几（范围0-6或者mon,tue,wed,thu,fri,stat,sun）"])
tb.add_row(["hour(int or str)", "时（0-23）"])
tb.add_row(["minute(int or str)", "分（0-59）"])
tb.add_row(["second(int or str)", "秒（0-59）"])
tb.add_row(["start_date(datetime or str)","最早开始日期（含）"])
tb.add_row(["end_date(datetime or str)","最晚结束日期（含）"])

print(tb)
print('\033[35m 请输入监测时间区间(多个时间则使用，分开。时间区间则使用-分开。)')
print("\033[35m 例如在每年 1-3、7-9 月份中的每个星期一、二中的 00:00, 01:00, 02:00 和 03:00 执行。"
      "则在month提示中输入1-2,7-9、在day提示中输入1,2 、在hour提示中输入0-3 、不需要输入的直接回车或者需要每小时或者每分钟等等触发输入*即可")

webhtml="https://github.com/huge-success/sanic" #页面展现

api="https://api.github.com/repos/channelcat/sanic"  #服务器数据文件

def getCron():
    global year
    global month
    global week
    global day_of_week
    global day
    global hour
    global minute
    global second
    global start_date
    global end_date
    print("请输入year!!")
    year=input()
    print("请输入month!!")
    month=input()
    print("请输入week！！")
    week=input()
    print("请输入day!!")
    day=input()
    print("请输入day_of_week!!")
    day_of_week=input()
    print("请输入hour!!")
    hour=input()
    print("请输入minute!!")
    minute=input()
    print("请输入second!!")
    second=input()
    print("请输入start_date!!")
    start_date=input()
    print("请输入end_date!!")
    end_date=input()
    if year=='':
        year=None
    if month=='':
        month=None
    if week=='':
        week=None
    if day=='':
        day=None
    if day_of_week=='':
        day_of_week=None
    if hour=='':
        hour=None
    if minute=='':
        minute=None
    if second=='':
        second=None
    if start_date=='':
        start_date=None
    if end_date=='':
        end_date=None

def monitor():
    # 开始检测
    oldDate=None
    while True:
        try:
            response=requests.get(api,timeout=7)
            # response=requests.get(api,timeout=7)
        except Exception as e:
            print(e)
        else:
            if response.status_code==200:
                newDate=response.json()["updated_at"]
                if oldDate==None:
                    oldDate=newDate
                if newDate>oldDate:
                    print("有数据更新")
                    broswer.open(webhtml)
                    # print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
            else:
                print("请求失败！！！")

def hello():
    print("hello")

def execute():
    getCron()

    job_defaults = {'max_instances': 5} #设置job同时运行，防止job运行时间大于调度周期时间

    # 最常用的两个调度器
    scheduler = BackgroundScheduler(timezone='MST', job_defaults=job_defaults) #此调度器并不会阻塞当前线程(异步),如果main线程结束则该线程也结束因此需要在main线程中加入模拟主进程持续运行代码块
    # scheduler = BlockingScheduler(timezone='MST', job_defaults=job_defaults) #调用start函数后会阻塞当前线程(同步)。当调度器是你应用中唯一要运行的东西时（如上例）使用。
    try:
        print(year,month,week,day,day_of_week,minute,second,start_date,end_date)
        scheduler.add_job(monitor, 'cron',  year=year,month=month,week=week,day=day, day_of_week=day_of_week,minute=minute,second=second,start_date=start_date, end_date=end_date)

        scheduler.start()

    except Exception as e:
        print(e)
        scheduler.shutdown()

if __name__ == '__main__':
    execute()

    # 模拟主进程持续运行
    try:
        while True:
            time.sleep(2)
            # print('sleep')
    except(KeyboardInterrupt, SystemExit):
        print('Exit The Job!')