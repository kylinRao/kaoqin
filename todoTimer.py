#coding=utf-8
import time,sched,os
#初始化sched模块的scheduler类
#第一个参数是一个可以返回时间戳的函数，第二个参数可以在定时未到达之前阻塞。
s = sched.scheduler(time.time,time.sleep)
#被周期性调度触发的函数
def event_func():
    print "todo running"
    os.system(r"E:\superTools\kaoqin-master\kaoqin.py")
#enter四个参数分别为：间隔事件、优先级（用于同时间到达的两个事件同时执行时定序）、被调用触发的函数，给他的参数（注意：一定要以tuple给如，如果只有一个参数就(xx,)）
def perform(inc):
    s.enter(inc,0,perform,(inc,))
    event_func()
def todo(inc=3600):
    s.enter(0,0,perform,(inc,))
    s.run()
if __name__ == "__main__":
    todo()
