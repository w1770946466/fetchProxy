#!/usr/bin/env python3
import time
from multiprocessing import Process, Manager, Semaphore
from clash import push, checkenv, filter
from check import check
from tqdm import tqdm
from init import init, cleanup
import subprocess


if __name__ == '__main__':
    with Manager() as manager:
        alive = manager.list()
        http_port, api_port, threads, source, timeout, outfile, proxyconfig, apiurl, testurl, config= init()
        clashname, operating_system = checkenv()
        print('Clash is Running on '+ operating_system)
        clash = subprocess.Popen([clashname, '-f', './temp/working.yaml', '-d', '.'])
        lenlines =len(config['proxies'])
        print('airport total == '+str(lenlines)+'\n')
        thread_max_num =threading.Semaphore(threads)
        thread_list = []
        #进度条添加
        bar = tqdm(total=lenlines, desc='Testing：')
        for line in lines:
            #为每个新URL创建线程
            t = threading.Thread(target=check, args=(alive,config['proxies'][line],apiurl,sema,timeout,testurl,bar))
            #加入线程池
            thread_list.append(t)
            #setDaemon()线程守护，配合下面的一组for...t.join(),实现所有线程执行结束后，才开始执行下面代码
            t.setDaemon(True)    #python多线程之t.setDaemon(True) 和 t.join()  https://www.cnblogs.com/my8100/p/7366567.html
            #启动
            t.start()

        #等待所有线程完成，配合上面的t.setDaemon(True)
        for t in thread_list:
            t.join()
        bar.close() #进度条结束
        """
        processes =[]
        sema = Semaphore(threads)
        time.sleep(5)
        for i in tqdm(range(int(len(config['proxies']))), desc="Testing"):
            sema.acquire()
            p = Process(target=check, args=(alive,config['proxies'][i],apiurl,sema,timeout,testurl))
            try:
                p.start()
                processes.append(p)
            except:
                continue
        for p in processes:
            p.join
        time.sleep(5)
        """
        alive=list(alive)
        push(alive,outfile)
        cleanup(clash)
