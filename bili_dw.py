import requests
import re
import os

#root = "D://pics//"
#reg = r'<img src="(.*?)" style="display:none;" class="cover_image"/>'
reg = r'<meta data-vue-meta="true" itemprop="thumbnailUrl" content="(.*?)"/>'
# def k(x):
# 	s = False
# 	while s != True:
# 		float_number = str(x)
# 		value = re.compile(r'^[-+]?[0-9]+$')
# 		result = value.match(float_number)
# 		if result:
# 			#print (float_number)
# 			s = True
# 			return float_number;
# 			#return 1;
# 		else:
# 			print("输入错误，请输入数字")
# 			return 0;

def gethtml(url):
    try:
        kv = {'user-agent':'Mozilla/5.0'}
        r = requests.get(url,headers=kv)
        r.raise_for_status()
        r.encoding = r.apparent_encoding
        return (r.text);
        print("爬取成功")
    except:
       print("爬取失败")

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
                print("文件保存成功 ",end="")
        else:
            print("文件已存在 ",end="")
    except:
        print("爬取失败")

def ds(reg,a):
    for i in re.findall(reg,a):
        #print(i)
        return(i)
    
# num = 0
# while num == 0:
#         num = k(input("请输入Bilibili视频av号："))
#         a = gethtml("https://www.bilibili.com/video/av%s/"%(num))
#         url = ds(reg,a)
#         download(url,root)
#         print("\n")
#         num = 0
       
# a = gethtml("https://www.bilibili.com/video/av%s/"%(num))
# url = ds(reg, a)
# download(url, root)

def bi(num,root):
    a = gethtml("https://www.bilibili.com/video/av%s/"%(num))
    url = ds(reg, a)
    print(url)
    download(url, root)

