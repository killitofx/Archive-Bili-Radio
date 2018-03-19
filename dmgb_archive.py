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


reg1 = r'��(.*?)��'
reg2 = r'��(.*?)��'
#reg3 = r'<meta data-vue-meta="true" itemprop="thumbnailUrl" content="(.*?)"/>'
reg4 = r'Av(.*?),'
reg5 = r'[0-9].(.*?)A'

homedir = os.getcwd()
mp3_dir = homedir + '\mp3'
mp4_dir = homedir + '\mp4'
work_locate = homedir
support_list = ['mp4']


logger = logging.getLogger("test.txt")   #����һ��logger,Ĭ��Ϊroot logger
logger.setLevel(logging.DEBUG)   #����ȫ��log����Ϊdebug��ע��ȫ�ֵ����ȼ����
hterm =  logging.StreamHandler()    #����һ���ն������handler,���ü���Ϊerror
hterm.setLevel(logging.INFO)
hfile = logging.FileHandler("access.log")    #����һ���ļ���¼��־��handler,���ü���Ϊinfo
hfile.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s  - %(levelname)s - %(message)s')   #����һ��ȫ�ֵ���־��ʽ
format_cs = logging.Formatter('[%(levelname)s]  %(message)s')
hterm.setFormatter(format_cs)   #����־��ʽӦ�õ��ն�handler
hfile.setFormatter(formatter)   #����־��ʽӦ�õ��ļ�handler
#logger.addHandler(hterm)    #���ն�handler��ӵ�logger
logger.addHandler(hfile)    #���ļ�handler��ӵ�logger

try:
    from bili_dw import *
except:
    logger.addHandler(hterm)


def check_diary(dir):
    check1 = os.path.exists(dir)
    if check1:
        logger.debug("%s�ļ������ҵ�" % dir)
        return

    else:
        logger.debug("δ����%s�ļ��У�����... " % dir)
        try:
            os.makedirs(dir)
            logger.debug("%s�����ɹ�" % dir)
        except:
            logger.error("%s����ʧ�ܣ�����Ȩ��" % dir)
            time.sleep(10)
            sys.exit()

def file_rename(name):
    term_name = m_name = ''
    #��ȡ��׺��
    suffix = '.' + name.split('.')[-1]
    #������
    if '��' in name:
        for x in re.findall(reg1, name):
            m_name = x
#            for i in x:
#                m_name += i
        if '����' in name:
            for i in re.findall(reg5, name):
                term_name = (i.replace('(', ''))
        elif '���' in name:
            for i in re.findall(reg5, name):
                term_name = (i.replace('(', ''))
        elif 'ȫһ��' in name:
            term_name = 'ȫһ��'
        elif '(��)'in name or '(��)'in name or '����'in name or '����' in name:
            for s in re.findall(reg5, name):
                term_name = (s.replace('(', ''))
                # term_name = term_name.replace("(", "")
                # term_name = term_name.replace(")", "")
        elif '��'in name:
            for y in re.findall(reg2, name):
                term_name = '��' + y[0] + '��'
        else:
            for s in re.findall(reg5, name):
                term_name = (s.replace('(', ''))
        new_name = m_name + term_name + suffix
        logger.info("�µ�����Ϊ %s" % new_name)
        run(name, m_name, new_name)

#name ԭ�� m_name �ļ����� new_name ������
def run(name,m_name,new_name):
    delay = random.randint(0, 100)/100
    time.sleep(delay)
    #�����ļ���
    logger.debug("task %s delay %s..." % (new_name, delay))
    logger.debug('Run task %s (%s)...' % (new_name, os.getpid()))
    start = time.time()
    os.rename(name, new_name)
    logger.info('�ļ�  %s  ������Ϊ  %s' % (name, new_name))
    check_diary(mp3_dir + '\\' + m_name)
    check_diary(mp4_dir + '\\' + m_name)
    #���ط���
    try:
        for z in re.findall(reg4, name):
            #print(z)
            bili_info = bi(z, mp3_dir + '\\' + m_name + '\\')
            #logger.info(bili_info)
            # bi(z, mp4_dir + '\\' + m_name + '\\')
            #�����ƶ��ļ��ķ�ʽ��С����������
            shutil.copy(mp3_dir + '\\' + m_name + '\\' + 'cover.jpg',mp4_dir + '\\' + m_name + '\\' + 'cover.jpg')
    except:
        logger.warning("���÷���������ʧ��")
    #����ffmpeg�����ӵ��ܵ�
    code = bulid_cfg(new_name, mp3_dir + '\\' + m_name + '\\' + new_name.replace('mp4', 'mp3'))
    #���ת��δ�����鵵�ļ�
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
        logger.info('%sת��ɹ�' %name)
        return 1
    else:
        logger.error('%sת��ʧ�ܣ�����Ϊ %s' % (name, cfg))


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
        logger.warning("\n\n�Ҳ���bili_d.py")
    if sys.argv.count('-p'):
        num = sys.argv.index('-p')
        p = int(sys.argv[num + 1])
        pool(p)
    else:
        pool()

