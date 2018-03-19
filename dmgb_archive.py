# coding=gbk
import os
import sys
import re
import logging
import time
import subprocess
import shutil
import random
from multiprocessing import Pool


reg1 = r'《(.*?)》'
reg2 = r'第(.*?)期'
#reg3 = r'<meta data-vue-meta="true" itemprop="thumbnailUrl" content="(.*?)"/>'
reg4 = r'Av(.*?),'
reg5 = r'[0-9].(.*?)A'

homedir = os.getcwd()
mp3_dir = homedir + '\mp3'
mp4_dir = homedir + '\mp4'
work_locate = homedir
support_list = ['mp4']


logger = logging.getLogger("test.txt")   #创建一个logger,默认为root logger
logger.setLevel(logging.DEBUG)   #设置全局log级别为debug。注意全局的优先级最高
hterm =  logging.StreamHandler()    #创建一个终端输出的handler,设置级别为error
hterm.setLevel(logging.INFO)
hfile = logging.FileHandler("access.log")    #创建一个文件记录日志的handler,设置级别为info
hfile.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s  - %(levelname)s - %(message)s')   #创建一个全局的日志格式
format_cs = logging.Formatter('[%(levelname)s]  %(message)s')
hterm.setFormatter(format_cs)   #将日志格式应用到终端handler
hfile.setFormatter(formatter)   #将日志格式应用到文件handler
#logger.addHandler(hterm)    #将终端handler添加到logger
logger.addHandler(hfile)    #将文件handler添加到logger

try:
    from bili_dw import *
except:
    logger.addHandler(hterm)


def check_diary(dir):
    check1 = os.path.exists(dir)
    if check1:
        logger.debug("%s文件夹已找到" % dir)
        return

    else:
        logger.debug("未发现%s文件夹，创建... " % dir)
        try:
            os.makedirs(dir)
            logger.debug("%s创建成功" % dir)
        except:
            logger.error("%s创建失败，请检查权限" % dir)
            time.sleep(10)
            sys.exit()

def file_rename(name):
    term_name = m_name = ''
    #获取后缀名
    suffix = '.' + name.split('.')[-1]
    #重命名
    if '《' in name:
        for x in re.findall(reg1, name):
            m_name = x
#            for i in x:
#                m_name += i
        if '番外' in name:
            for i in re.findall(reg5, name):
                term_name = (i.replace('(', ''))
        elif '完结' in name:
            for i in re.findall(reg5, name):
                term_name = (i.replace('(', ''))
        elif '全一期' in name:
            term_name = '全一期'
        elif '(上)'in name or '(下)'in name or '上期'in name or '下期' in name:
            for s in re.findall(reg5, name):
                term_name = (s.replace('(', ''))
                # term_name = term_name.replace("(", "")
                # term_name = term_name.replace(")", "")
        elif '第'in name:
            for y in re.findall(reg2, name):
                term_name = '第' + y[0] + '期'
        else:
            for s in re.findall(reg5, name):
                term_name = (s.replace('(', ''))
        new_name = m_name + term_name + suffix
        logger.info("新的名字为 %s" % new_name)
        run(name, m_name, new_name)

#name 原名 m_name 文件夹名 new_name 新名字
def run(name,m_name,new_name):
    delay = random.randint(0, 100)/100
    time.sleep(delay)
    #建立文件夹
    logger.debug("task %s delay %s..." % (new_name, delay))
    logger.debug('Run task %s (%s)...' % (new_name, os.getpid()))
    start = time.time()
    os.rename(name, new_name)
    logger.info('文件  %s  重命名为  %s' % (name, new_name))
    check_diary(mp3_dir + '\\' + m_name)
    check_diary(mp4_dir + '\\' + m_name)
    #下载封面
    try:
        for z in re.findall(reg4, name):
            #print(z)
            bili_info = bi(z, mp3_dir + '\\' + m_name + '\\')
            #logger.info(bili_info)
            # bi(z, mp4_dir + '\\' + m_name + '\\')
            #采用移动文件的方式减小服务器负载
            shutil.copy(mp3_dir + '\\' + m_name + '\\' + 'cover.jpg',mp4_dir + '\\' + m_name + '\\' + 'cover.jpg')
    except:
        logger.warning("调用封面下载器失败")
    #创建ffmpeg命令，添加到管道
    code = bulid_cfg(new_name, mp3_dir + '\\' + m_name + '\\' + new_name.replace('mp4', 'mp3'))
    #如果转码未出错，归档文件
    if code:
        shutil.move(new_name, mp4_dir + '\\' + m_name)
    end = time.time()
    logger.debug('Task %s runs %0.2f seconds.' % (new_name, (end - start)))

def bulid_cfg(name, locate):
    cfg = 'ffmpeg -i data1 -vn  -acodec libmp3lame -ac 2 -qscale:a 4 -ar 48000  data2'
    cfg = cfg.replace('data1', name)
    cfg = cfg.replace('data2', locate)
    logger.debug(cfg)
    returnCode = subprocess.call(cfg, shell=True, stdin=subprocess.PIPE)
    if not returnCode:
        logger.info('%s转码成功' %name)
        return 1
    else:
        logger.error('%s转码失败，命令为 %s' % (name, cfg))


def pool(p = 8):
    p = Pool(p)
    for i in os.listdir(work_locate):
        for k in support_list:
            if k in i:
                p.apply_async(file_rename, args=(i,))
    p.close()
    p.join()



if __name__=='__main__':
    logging.info("\n\n")
    check_diary(mp3_dir)
    check_diary(mp4_dir)
    if not os.path.exists(homedir + "/bili_dw.py"):
        logger.addHandler(hterm)
        logger.warning("\n\n找不到bili_d.py")
    if sys.argv.count('-p'):
        num = sys.argv.index('-p')
        p = int(sys.argv[num + 1])
        pool(p)
    else:
        pool()

