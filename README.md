# bilibili广播剧归档
这是一个帮喜欢听不可描述的广播剧的妹妹写的程序<br>
本程序能帮助归档从bilibili上的下载的广播剧大户SLXZ的广播剧，化简名称并转码成mp3，归档<br>
唯一指定下载器 jjdownload <a href="http://client.jijidown.com/">下载地址</a><br>
运行环境<br>
python运行环境<br>
python3.6<br>
ffmpeg<br>
ffmpeg 在jjdownload/OrderEXE中有，复制到根目录（dmgb_archive.py所在目录）或者把ffmpeg添加到环境变量<br>

<h1>启动方式</h1>
0、安装python运行环境<br>
1、复制ffmpeg到指定目录或把ffmpeg添加到环境变量<br>
2、把下载的视频放到run.bat的目录下<br>
3、运行run.bat<br>
4、默认会创建一个mp3文件夹和一个mp4文件夹<br>
<br>
<h1>注意事项</h1>
不要放在桌面/用户文件夹运行，会被Defender屏蔽<br>
要下载封面，必须使用jj下载视频，该程序会检测文件名中的Av号，根据Av号下载封面<br>
av号的正则表达式为'Av(.*?),'<br>
<br>
<h1>附加功能</h1><br>
b站封面下载<br>
0、安装python运行环境<br>
1、打开c.bat<br>
2、输入python bili_dw.py 170001<br>
3、170001为av号 默认下载地址为d://pics<br>
4、附加参数<br>
-l 指定下载地址 例如 python bili_dw.py 170001 -l D:// 下载到d盘根目录<br>
-n 指定文件名   例如 python bili_dw.py 170001 -n cover 下载的文件名为cover.jpg<br>
不推荐使用<br>
<del>-r 指定正则表达式 可使用-r自定义正则  (.*?)为需要提取的地址</del><br>
