# coding=gbk
import os, sys, re, logging, time, subprocess, shutil, requests
from bili_dw import *

reg1 = r'��(.*?)��'
reg2 = r'��(.*?)��'
reg3 = r'<meta data-vue-meta="true" itemprop="thumbnailUrl" content="(.*?)"/>'
reg4 = r'Av(.*?),'
#reg5 = r''
reg5 = r'[0-9].(.*?)A'

homedir = os.getcwd()
mp3_dir = homedir + '\mp3'
mp4_dir = homedir + '\mp4'
work_locate = homedir
support_list = ['mp4']


logging.basicConfig(level = logging.DEBUG, format = '%(levelname)s - %(asctime)s - %(message)s')
logger = logging.getLogger(__name__)
logger.setLevel(level = logging.INFO)


def check_diary(dir):
    check1 = os.path.exists(dir)
    if check1:
        logging.info("%s�ļ������ҵ�" % dir)
    else:
        logging.info("δ����%s�ļ��У�����... " % dir)
        try:
            os.makedirs(dir)
            logging.info("�����ɹ�")
        except:
            logging.error("����ʧ�ܣ�����Ȩ��")
            input()
            sys.exit()

def file_rename(name):
    term_name = m_name = ''
    suffix = '.' + name.split('.')[-1]
    if '��' in name:
        for x in re.findall(reg1, name):
            for i in x:
                m_name += i

        if '����' in name:
            for i in re.findall(reg5, name):
                term_name = (i.replace('(', ''))
        elif '���' in name:
            for i in re.findall(reg5, name):
                term_name = (i.replace('(', ''))
        elif 'ȫһ��' in name:
            term_name = 'ȫһ��'
        elif '��':
            for y in re.findall(reg2, name):
                term_name = '��' + y[0] + '��'
        else:
            for i in re.findall(reg5, name):
                term_name = (i.replace('(', ''))
        new_name = m_name + term_name + suffix
        #print(new_name)

        os.rename(name, new_name)
        logging.info('�ļ�  %s  ������Ϊ  %s' % (name, new_name))
        check_diary(mp3_dir + '\\' + m_name)
        check_diary(mp4_dir + '\\' + m_name)

        for z in re.findall(reg4,name):
            print(z)
            bi(z,mp3_dir + '\\' + m_name + '\\')
            bi(z, mp4_dir + '\\' + m_name + '\\')

        code = bulid_cfg(new_name, mp3_dir + '\\' +m_name+ '\\' + new_name.replace('mp4', 'mp3'))

        if code:
            shutil.move(new_name, mp4_dir + '\\' + m_name)

def bulid_cfg(name, locate):
    cfg = 'ffmpeg -i data1 -vn  -acodec libmp3lame -ac 2 -qscale:a 4 -ar 48000  data2'
    cfg = cfg.replace('data1', name)
    cfg = cfg.replace('data2', locate)
    logging.info(cfg)
    returnCode = subprocess.call(cfg, shell=True, stdin=subprocess.PIPE)
    if not returnCode:
        logging.info('%sת��ɹ�' %name)
        return 1
    else:
        logging.error('%sת��ʧ�ܣ�����Ϊ %s' % (name, cfg))


check_diary(mp3_dir)
check_diary(mp4_dir)
for i in os.listdir(work_locate):
    for k in support_list:
        if k in i:
            file_rename(i)
            for x in re.findall(reg1, i):
                print(x)


