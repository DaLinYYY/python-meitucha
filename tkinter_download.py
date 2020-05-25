import os
import urllib.request
from bs4 import BeautifulSoup
import json
import re
import queue
import threading
import tkinter as tk
import tkinter.messagebox
import socket
# base_url = "https://www.meitucha.com/t/5475/"
# search = "面饼仙儿"


def get_json1(input1, input2, txt):
    base_url = input1.get()
    search = input2.get()
    if not os.path.exists(search):
        os.makedirs(search)
    count = 1
    for i in range(1, 100):
        url = base_url + "?page=" + str(i)
        # 创建request对象
        request = urllib.request.Request(url)
        # 添加header
        request.add_header('user-agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/'
                                         '537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36')
        # 发送请求获取结果
        response = urllib.request.urlopen(request)
        response = response.read().decode("utf-8")

        bs = BeautifulSoup(response, "html.parser")  # 缩进格式
        data1 = {}
        if len(bs.select_one('.hezi').get_text()) > 3:
            for qt in bs.select_one('.hezi').select('li'):
                data1['page'] = qt.select('span')[0].get_text()
                data1['title'] = qt.select('p')[3].select('a')[0].get_text()
                data1['url'] = "https://www.meitucha.com" + qt.select('a')[0].attrs['href']
                # data1['model'] = qt.select('p')[1].select('a')[0].get_text()
                # data1['company'] = qt.select('p')[0].select('a')[0].get_text()
                json_str = json.dumps(data1)
                with open(search + '/' + str(count) + '.json', 'w') as json_file:
                    json_file.write(json_str)
                print("成功写入第" + str(count) + "个文件")
                txt.insert(tk.END, "成功写入第{}个文件\n".format(str(count)))
                txt.see(tk.END)
                count += 1

        else:
            print("写真URL采集完成")
            txt.insert(tk.END, "写真URL采集完成，请点击第二步\n")
            txt.see(tk.END)
            break


def get_json2(input2, txt):
    search = input2.get()
    if not os.path.exists(search + '/00URL备份'):
        os.makedirs(search + '/00URL备份')

    urlQueue = queue.Queue(2000)

    for t in range(1, 2000):
        if os.path.exists(search + '/' + str(t) + '.json'):
            urlQueue.put(t)

    threads = []
    threadNum = 8
    for i in range(0, threadNum):
        t = threading.Thread(target=down, args=(urlQueue, search, txt))
        threads.append(t)
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    print("图片地址保存成功，请点击第三步")
    txt.insert(tk.END, "图片地址保存成功，请点击第三步\n")
    txt.see(tk.END)


def down(url_num, search, txt):

    patten = "http://cdn.xie2.com/a/1/\w+/"
    while True:
        try:
            t1 = url_num.get_nowait()
        except Exception as e:
            print(e)
            break
        f1 = open(search + '/' + str(t1) + '.json', 'r')
        file = f1.read()
        json_str = json.loads(file)
        data1 = {'title': json_str['title'], 'url': json_str['url'], 'page': json_str['page']}

        url2 = []
        url = str(data1['url'])
        request1 = urllib.request.Request(url)
        request1.add_header('user-agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/'
                                          '537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36')
        socket.setdefaulttimeout(30)
        # 发送请求获取结果
        try:
            response1 = urllib.request.urlopen(request1)
            response1 = response1.read().decode("utf-8")
            qt1 = BeautifulSoup(response1, "html.parser")  # 缩进格式

            src = qt1.select_one('.content').select('img')[0].attrs['src']
            num111 = re.search(patten, src).group(0)
            # print(num111)
            page = data1['page'][:-1]
            for iq in range(1, int(page) + 1):
                url2.append(str(num111) + str(iq) + '.jpg')
            data1['url1'] = url2
            json_str = json.dumps(data1)
            with open(search + '/a' + str(t1) + '.json', 'w') as json_file:
                json_file.write(json_str)
            with open(search + '/00URL备份' + '/a' + str(t1) + '.json', 'w') as json_file:
                json_file.write(json_str)
            print('当前线程为：' + threading.currentThread().name + "成功写入第" + str(t1) + "个文件")
            txt.insert(tk.END, "当前线程为{}，成功写入第{}个文件\n".format(threading.currentThread().name, str(t1)))
            txt.see(tk.END)
            f1.close()
            os.remove(search + '/' + str(t1) + '.json')
        except socket.timeout:
            print("请求网页失败")
            txt.insert(tk.END, "请求网页失败\n")
            url_num.put_nowait(t1)


def down_ultra(input2, txt, thread):
    threadNum = int(thread.get())
    search = input2.get()
    urlQueue = queue.Queue(2000)

    for t in range(1, 2000):
        if os.path.exists(search + '/a' + str(t) + '.json'):
            urlQueue.put(t)

    threads = []

    for i in range(0, threadNum):
        t = threading.Thread(target=down1, args=(urlQueue, search, txt))
        threads.append(t)
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    print("真棒！采集完成啦。\n")
    txt.insert(tk.END, "真棒！采集完成啦。\n")
    txt.see(tk.END)


def down1(url_num, search, txt):

    while True:
        try:
            # 不阻塞读取列表
            t1 = url_num.get_nowait()
        except Exception as e:
            print(e)
            break
        f1 = open(search + '/a' + str(t1) + '.json', 'r')
        file = f1.read()
        json_str = json.loads(file)
        data1 = {'title': json_str['title'], 'url': json_str['url'], 'page': json_str['page'], 'url1': json_str['url1']}
        if os.path.exists(search + '/[' + data1['page'] + ']' + data1['title']):

            print("目录已存在:" + data1['title'])
            txt.insert(tk.END, "目录已存在:{}\n".format(data1['title']))
            txt.see(tk.END)
        else:
            os.makedirs(search + '/[' + data1['page'] + ']' + data1['title'])
            print("创建目录:" + data1['title'])
            txt.insert(tk.END, "创建目录:{}\n".format(data1['title']))
            txt.see(tk.END)

        count = 1
        for qqq in data1['url1']:
            socket.setdefaulttimeout(30)
            try:
                urllib.request.urlretrieve(qqq, search + '/[' + data1['page'] + ']' +
                                           data1['title'] + "/" + str(count) + '.jpg')
                print(threading.currentThread().name + "保存进度：" + str(count) + 'P/' + data1['page'] + "张图片")
                txt.insert(tk.END,
                           "{}保存进度：{}P/{}张图片\n".format(threading.currentThread().name, str(count), data1['page']))
                txt.see(tk.END)
                count += 1
            except socket.timeout:
                print("保存图片失败")
                txt.insert(tk.END, "保存图片失败\n")
                url_num.put_nowait(t1)

        f1.close()
        # 判断是否下载完整
        page = data1['page'][:-1]
        if len(os.listdir(search + '/[' + data1['page'] + ']' + data1['title'])) == int(page):
            os.remove(search + '/a' + str(t1) + '.json')
            print("第" + str(t1) + "个写真集已经采集完成，继续采集下一个")
            txt.insert(tk.END, "第{}个写真集已经采集完成，继续采集下一个\n".format(t1))
            txt.see(tk.END)


# get_json1(search, base_url)
# get_json2(search)
# down_ultra(search)

def thread_it(func, *args):
    t1 = threading.Thread(target=func, args=args)
    t1.setDaemon(True)
    t1.start()


def message():
    tkinter.messagebox.showinfo('帮助', '第一步：获取写真URL，第二步：获取每张图片的URL，第三步：多线程下载。依次点击三个按钮可以保证图片下载的完整性')


def gui():
    windows = tk.Tk()
    windows.title('美图查图片下载器')  # 窗口标题
    windows.geometry("700x500+500+300")  # 窗口大小

    tk.Label(windows, text="下载地址：", font=13).place(x=10, y=30)  # 贴标签
    tk.Label(windows, text="文件夹名称：", font=13).place(x=10, y=80)  # 贴标签
    tk.Label(windows, text="线程数(建议为4):", font=13).place(x=350, y=80)
    # 输入框
    base_url = tk.StringVar()
    e1 = tk.Entry(windows, textvariable=base_url)
    e1.place(x=110, y=30, width=300)
    search = tk.StringVar()
    e2 = tk.Entry(windows, textvariable=search)
    e2.place(x=110, y=80, width=150)
    threadNum = tk.StringVar()
    e3 = tk.Entry(windows, textvariable=threadNum)
    e3.place(x=500, y=80, width=50)
    e3.insert(tk.END, 4)
    # 帮助框
    tk.Button(windows, text='帮助', command=message).place(x=620, y=50)

    # 三个下载按钮
    tk.Button(windows, text='第一步', command=lambda: thread_it(get_json1, base_url, search, txt)).place(x=100, y=150)
    tk.Button(windows, text='第二步', command=lambda: thread_it(get_json2, search, txt)).place(x=300, y=150)
    tk.Button(windows, text='第三步', command=lambda: thread_it(down_ultra, search, txt, threadNum)).place(x=500, y=150)

    # 消息框
    txt = tk.Text(windows)
    txt.place(x=50, y=250, width=600, height=240)

    windows.mainloop()


if __name__ == "__main__":
    gui()
