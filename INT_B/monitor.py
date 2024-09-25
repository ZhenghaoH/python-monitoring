# -*- coding: UTF-8 -*-
import psutil
import GPUtil
import socket
import os
import time
import pymysql.cursors
import time
from datetime import datetime
import json


# def get_network_bytes(interface='eth0'):
#     # 获取指定接口的字节流量统计
#     net_io = psutil.net_io_counters(pernic=True)
#     return net_io[interface].bytes_sent, net_io[interface].bytes_recv

# def measure_bandwidth(interface='eth0', duration=1):
#     # 获取初始字节数
#     bytes_sent_start, bytes_recv_start = get_network_bytes(interface)
#     # 等待指定时间间隔
#     time.sleep(duration)
#     # 获取结束字节数
#     bytes_sent_end, bytes_recv_end = get_network_bytes(interface)
#     # 计算流量（字节）
#     sent_bytes = bytes_sent_end - bytes_sent_start
#     recv_bytes = bytes_recv_end - bytes_recv_start
#     # 将流量转换为 Gbps
#     sent_mbps = (sent_bytes * 8) / (1024 * 1024 * 1024 * duration)
#     recv_mbps = (recv_bytes * 8) / (1024 * 1024 * 1024 * duration)
#     return sent_mbps, recv_mbps

def monitor_txt():
    #hostname = socket.gethostname()
    #print("Hostname:", hostname)
    #hostname = os.getenv('HOSTNAME')
    #print("Mininet Hostname:", hostname)

    #内存
    mem = psutil.virtual_memory()
    # 系统总计内存
    zj = float(mem.total) / 1024 / 1024 
    # 系统已经使用内存
    ysy = float(mem.used) / 1024 / 1024 
    # 系统空闲内存
    kx = float(mem.free) / 1024 / 1024 

    cpu = (str(psutil.cpu_percent(interval=0.5))) + '%'
    GPUs = GPUtil.getGPUs()

    # interface = 'eth0'  # 替换为你要测量的网络接口名称
    # sent_gbps, recv_gbps = measure_bandwidth(interface, duration=1)
    #print(f"Sent: {sent_mbps:.2f} Gbps, Received: {recv_mbps:.2f} Gbps")

    CPU_count = psutil.cpu_count(logical=False) #CPU核数
    CPU_percent = cpu #CPU使用率
    Memory_total = zj  #总内存
    Memory_percent = mem.percent #内存使用率
    if len(GPUs) == 0:
        GPU = 0
    else:
        GPU = 1


    #将感知信息写入txt文件
    with open('node-info.txt', 'w') as f:
        print("DUID:1", file=f)

        # 查看cpu信息
#        print("主频: %s" %psutil.cpu_freq().current,file = f)
        print(u"CPU_count: %s" % psutil.cpu_count(logical=False), file=f)
#        print(u"CPU线程数: %s" % psutil.cpu_count(), file=f)
        print(u"CPU_percent: %s" % cpu, file=f)
#
        # 写入内存信息
        print('Memory_total:%.2fMB' % zj, file=f)
#        print('已使用内存:%.2fMB' % ysy,  file=f)
        print('Memory_percent:%s' % mem.percent, file=f)

        #写入磁盘信息
       # disk_partion = psutil.disk_partitions()
        #for i in range(len(disk_partion)):
         #   disk_path = str(disk_partion[i]).split('device=\'')[1].split('\'')[0]
          #  print(disk_path + '磁盘容量：%s'  %psutil.disk_usage(disk_path).total, file=f)
           # print(disk_path + '磁盘占用率：%s'  %psutil.disk_usage(disk_path).percent, file=f)

        #写入GPU信息
        if len(GPUs) == 0:
            print("GPU:0", file=f)
        else:
            print("GPU:1", file=f)
#        for i in range(len(GPUs)):
#            print('GPU型号:'+ GPUs[i].name, file=f)
#            print('GPU负载:'+ str(GPUs[i].load), file=f)
#            print('显存利用率:'+ str(GPUs[i].memoryUtil), file=f)

        #写入流量信息
        # print("sent_gbps:%.2fGbps" % sent_gbps, file=f)
        # print("recv_gbps:%.2fGbps" % recv_gbps, file=f)




monitor_txt()
