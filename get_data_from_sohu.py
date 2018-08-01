#!/usr/bin/env python
# -*- coding: utf-8 -*-

import codecs
from bs4 import BeautifulSoup
import sys
from datetime import datetime
import uuid
from selenium import webdriver
import time, re, os
import platform
from get_gif_text import get_text_and_gif

reload(sys)
sys.setdefaultencoding('utf8')


def getHtmlSource(url):
    driver = webdriver.PhantomJS(executable_path="phantomjs-2.1.1-linux-x86_64/bin/phantomjs")
    time.sleep(2)
    driver.get(url)  # 获取网页
    return driver.page_source


def get_url_data(url):
    result=dict()
    #浏览器模拟下载js渲染的html源码
    fp_w = codecs.open("sohus", 'w', encoding="utf-8")
    html = getHtmlSource(url)
    sout = BeautifulSoup(html, 'lxml')
    texts = sout.body
    print >> fp_w, texts
    # 读取网页源码信息
    fp_r = codecs.open("sohus", 'r', encoding="utf-8")
    text = []
    for line in fp_r.readlines():
        text.append(line.strip().decode("utf-8"))
    #分析html
    patt = re.compile("https.+?\"")
    for line in text:
        if re.search(patt, line):
            page_url = re.findall(patt, line)[0].replace("\"", "")
            result[page_url] = line.strip()
            print page_url,line.strip()
    return result

if __name__ == '__main__':
    #url = ur'http://sports.sohu.com/s2018/2018wcespvsrus/'
    url = "http://sports.sohu.com/s2018/2018wcbelvsjpn/"
    games = [(u'西班牙', u'俄罗斯'), (u'克罗地亚', u'丹麦'), (u"巴西", u'墨西哥'),(u'比利时',u'日本')]
    scores = re.compile(u'(\d)(-|:|：)(\d)')
    scores2 = re.compile(u'场\d+?球')
    score3 = re.compile(u"\d+?强")
    urls_dict = get_url_data(url)
    for src,text in urls_dict.items():
        flag = False
        for game1, game2 in games:
            if game1 in text and game2 in text:
                flag = True
            if (scores.search(text) or scores2.search(text) or score3.search(text)) and (game1 in text or game2 in text):
                flag = True
            if flag:
                directory = "sohu/" + "-".join([game1, game2])
                while os.path.exists(directory):
                    directory += "0"
                print "download ...  url={}".format(src)
                get_text_and_gif(url=src, save_path_director=directory, class_structure=".article")
                print "finished url={}".format(src)
            break
