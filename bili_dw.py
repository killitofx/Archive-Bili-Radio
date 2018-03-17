import requests
import re
import os
import logging


reg = r'<meta data-vue-meta="true" itemprop="thumbnailUrl" content="(.*?)"/>'
def gethtml(url):
    try:
        kv = {'user-agent':'Mozilla/5.0'}
        r = requests.get(url,headers=kv)
        r.raise_for_status()
        r.encoding = r.apparent_encoding
        return (r.text);
        logging.info("网页下载成功")
    except:
       logging.error("网页下载失败")

def download(url,root):
    #path = root + url.split('/')[-1]
    path = root + 'cover' + '.' + url.split('.')[-1]
    try:
        if not os.path.exists(root):
            os.mkdir(root)
        if not os.path.exists(path):
            r = requests.get(url)
            #time.sleep(0.5)
            with open(path, 'wb') as f:
                f.write(r.content)
                f.close()
                logging.info("封面保存成功%s" % path)
                return "封面保存成功%s" % path
        else:
            logging.warning("封面已存在%s" % path)
            return "封面已存在%s" % path
    except:
        logging.error("封面下载失败")
        return "封面下载失败"

def ds(reg,a):
    for i in re.findall(reg,a):
        #print(i)
        return(i)


def bi(num,root):
    a = gethtml("https://www.bilibili.com/video/av%s/"%(num))
    url = ds(reg, a)
    logging.info(url)
    info = download(url, root)
    return info

