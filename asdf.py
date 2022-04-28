#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 28 10:38:00 2022

@author: tup0lev
"""

from __future__ import unicode_literals
from googletrans import Translator, constants
from pprint import pprint
import random
from biliup.plugins.bili_webup import BiliBili, Data
from bs4 import BeautifulSoup
import urllib.request
import re
from google.cloud import translate_v2
import youtube_dl


def getVid(): # get random youtube video
    print("获取一个0播放的youtube视频")
    
    fp = urllib.request.urlopen("https://petittube.com/") #get random unwatched utb vid
    mybytes = fp.read()
    mystr = mybytes.decode("utf8")
    fp.close()
    vidID = mystr.partition("embed/")[2].rpartition("?version")[0] 
    youtubeurl= "https://www.youtube.com/watch?v=" + vidID
    print(   "youtube视频地址是"   +  youtubeurl     )
    return(youtubeurl)

def validateVid(vidurl):
    print("检查重复获取")
    
    with open('cked.txt') as f:
        lines = f.readlines()
        print(lines)
    for line in lines:
        if vidurl == line:
            print("已经获取过")
            return False
    vidfile = open('cked.txt', 'a')
    vidfile.write("\n")
    vidfile.write(vidurl)
    vidfile.close()
    
    print("检查视频成分")
    soup = BeautifulSoup(urllib.request.urlopen(vidurl))
    print ("视频标题为" + soup.title.string)
    title = soup.title.string.replace("- YouTube", "").replace("#", "")
    print("检查视频标题是否有汉字")
    for _char in soup.title.string:
        if '\u4e00' <= _char <= '\u9fa5':
            print("视频标题有汉字，8行")
            #utb上中文视频大都是台巴子发的，太容易政治不正确
            #因此只要有汉字就一棒子打死
            return False
    print("视频标题没有汉字, 好耶！")
    print("检查视频标题是不是英文")#为什么要检查是不是英文捏？
    #因为调试需要，其他语言没法检查机翻的质量捏
    translator = Translator()
    print(translator.detect(title))
    if (translator.detect(title).lang) != "en" :
        print("不是英文捏")
        return False
    translation = translator.translate(title, dest='zh-CN')    
    print("机翻完了的超尬标题是: " + translation.text)
    print("开始简单审查视频-关键词匹配")

    #TODO 
    #暂时先8做这个了
    print("顺利通过成分检查")
    return True 


def downloadVid(vidurl):
    print("下载视频")
    
    ydl_opts = {
    'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]',       
    'outtmpl': 'Download',        
    'noplaylist' : True,        
    'postprocessors': [{
    'key': 'FFmpegVideoConvertor',
    'preferedformat': 'mp4'
    }]
    }
    
    
    
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([vidurl])
    

    
    #TODO
    pass

def uploadvid():
    print("上传视频到霹雳霹雳")
    #TODO
    pass


while (True):
    my_vid = getVid() #获取视频

    if ( validateVid(my_vid) ): #审查视频
        downloadVid(my_vid)
        uploadvid()
 
