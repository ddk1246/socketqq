import threading, time, random


class Messy:
    def __init__(self):
        self.__messy = 0

    def m(self, i):
        # 随机时间进行打印
        time.sleep(random.random() * 2)
        print(i)
        if i == 1:
            self.__messy = 1

    def main(self):
        Threads = []
        # 将会启动10个线程,线程id为 1 时全部线程终止！
        for i in range(10):
            t = threading.Thread(target=self.m, args=(i,))
            t.daemon = 1
            Threads.append(t)
        # 启动所有线程
        for i in Threads:
            i.start()
        # 当标志位【 messy 】时所有多线程结束
        while 1:
            if self.__messy:
                break
        print('线程已退出!')


Messy().main()
# 继续执行后续程序
for i in range(5):
    print('yeah!')
