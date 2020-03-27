import re
import socket
import time
import threading
import requests
import json
import csv


class SpiderDanmu(object):
    def __init__(self, roomid):
        self.roomid = roomid
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        url = "openbarrage.douyutv.com"
        port = 8601
        host = socket.gethostbyname(url)
        self.client.connect((host, port))
        self.patterndanmu = re.compile(b'type@=chatmsg.*?/uid@=(.+?)/.*?/txt@=(.*?)/cid@')
        self.patterngift = re.compile(b'gfid@=(.+?)/.+?/uid@=(.+?)/.+?/gfcnt@=(.+?)/.*?hits@=(.+?)/')
        self.fname = "room" + str(roomid)
        self.last_keeplive_time = time.time()  # 上次心跳包发送的时间

    # 根据协议格式处理信息并发送
    def send_msg(self, msgstr):
        msg = msgstr.encode('utf-8')
        data_len = len(msg) + 8
        code = 689
        # 构造协议头
        msghead = int.to_bytes(data_len, 4, 'little') + int.to_bytes(data_len, 4, 'little') + int.to_bytes(code, 4,
                                                                                                           'little')
        # 发送协议头、消息请求
        self.client.send(msghead)
        self.client.send(msg)

    # 登录并进入某房间，获取弹幕
    def join_get(self):
        # 登录
        login_msg = "type@=loginreq/roomid@={}/\0".format(self.roomid)
        self.send_msg(login_msg)
        # 加入房间
        join_msg = "type@=joingroup/rid@={}/gid@=-9999/\0".format(self.roomid)
        self.send_msg(join_msg)

        kplive = threading.Thread(name="room_keep" + str(self.roomid), target=self.keeplive)
        kplive.setDaemon(True)
        kplive.start()
        # 匹配弹幕，最短匹配
        print(str(self.roomid) + "登录")
        data_list = []

        while True:  # True

            if (time.time() - self.last_keeplive_time > 60):  # 如果一分钟内没有发送过心跳包了，则线程结束
                break

            # 返回信息，拼合
            buffer = b''
            while True:
                recv_data = self.client.recv(4096)
                buffer += recv_data
                if recv_data.endswith(b'\x00'):
                    break

            # 弹幕 0
            if re.search(b'type@=chatmsg', buffer):
                dms = self.patterndanmu.findall(buffer)
                for i in dms:
                    uid = i[0].decode(encoding='utf-8', errors='ignore')
                    dm = i[1].decode(encoding='utf-8', errors='ignore')
                    danmu = {
                        'flag': 0,
                        'uid': uid,
                        'content': dm,
                        'time': time.time(),
                    }
                    data_list.append(danmu)
                    with open("data/" + self.fname + "danmu.csv", 'a', encoding='utf-8', newline='') as f:
                        writer = csv.writer(f)
                        writer.writerow((0, uid, dm, time.time()))
                    # print(danmu)

            # 礼物1
            if re.search(b'type@=dgb', buffer):
                gifts = self.patterngift.findall(buffer)
                for i in gifts:
                    uid = i[1].decode(encoding='utf-8', errors='ignore')
                    gid = i[0].decode(encoding='utf-8', errors='ignore')
                    gfcnt = i[2].decode(encoding='utf-8', errors='ignore')
                    hits = i[3].decode(encoding='utf-8', errors='ignore')
                    gift = {
                        'flag': 1,
                        'uid': uid,
                        'content': gid,
                        'gfcnt': gfcnt,
                        'hits': hits,
                        'time': time.time(),
                    }
                    with open("data/" + self.fname + "gift.csv", 'a', encoding='utf-8', newline='') as f:
                        writer = csv.writer(f)
                        writer.writerow((0, uid, gid, gfcnt, hits, time.time()))

            time.sleep(0.05)

        print("end!")

    # 心跳
    def keeplive(self):
        while (True):
            self.last_keeplive_time = time.time()
            live_msg = 'type@=mrkl/\0'
            self.send_msg(live_msg)
            time.sleep(30)


def thread_restart():
    while (True):
        global threadlist
        dellist = []
        addlist = []
        for x in threadlist:
            if (x.is_alive() == False):
                num = int(x.name[4:])
                s = SpiderDanmu(num)
                k = threading.Thread(name=x.name, target=s.join_get)
                print("启动线程" + x.name)
                k.start()

                dellist.append(x)
                addlist.append(k)
        for d in dellist:
            threadlist.remove(d)
        for a in addlist:
            threadlist.append(a)
        time.sleep(60)


def thread_status():
    while (True):
        global threadlist
        for x in threadlist:
            if (x.is_alive == False):
                print(x.name, x.is_alive())
        timeArray = time.localtime(time.time())
        otherStyleTime = time.strftime("%Y--%m--%d %H:%M:%S", timeArray)
        print(otherStyleTime)
        time.sleep(30)


if __name__ == '__main__':

    global roomlist
    global threadlist

    threadlist = []
    # 最多2000左右
    roomlist = [36252]

    for i in roomlist:
        s = SpiderDanmu(i)
        x = threading.Thread(name="room" + str(i), target=s.join_get)
        threadlist.append(x)
        x.start()
        # time.sleep(0.5)

    t1 = threading.Thread(name="进程状态", target=thread_status)
    t2 = threading.Thread(name="进程重启", target=thread_restart)
    print("t1t2启动")
    t1.start()
    t2.start()
