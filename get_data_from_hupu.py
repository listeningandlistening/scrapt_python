#!/usr/bin/env python
# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import re,os
import time
import json
import random
import logging
from get_gif_text import get_text_and_gif


def get_target_urls(url):
    urls_dict = dict()
    try:
        request = requests.get(url,verify=False,timeout=10)
    except requests.exceptions.Timeout:
        print 'timeout'
        return ''
    try:
        #解析访问得到的html页面
        soup = BeautifulSoup(request.text,"html.parser")
    except:
        print 'BeautifulSoup err'
        return ''
    fouce_news = soup.select('div[class="fouce-news"]')
    news_list = fouce_news[0].select('a')
    for news in news_list:
        src = news.attrs['href']
        text = news.get_text()
        urls_dict[text] = src
    return urls_dict

if __name__=='__main__':
    url = 'https://soccer.hupu.com/'
    games = [(u'西班牙', u'俄罗斯'), (u'克罗地亚', u'丹麦'), (u"巴西", u'墨西哥'),(u'比利时',u'日本'),(u'英格兰',u'哥伦比亚'),(u'瑞典',u'瑞士')]
    scores = re.compile(u'(\d)(-|:|：)(\d)')
    scores2 = re.compile(u'场\d+?球')
    scores3 = re.compile(u"\d+?强")
    urls_dict = get_target_urls(url)
    for text, src in urls_dict.items():
        flag=False
        for game in games:
            if game[0] in text and game[1] in text:
                flag=True
            if (scores.search(text) or scores2.search(text) or scores3.search(text)) and (game[0] in text or game[1] in text):
                flag=True
            if flag:
                try:
                    directory="hupu/"+"-".join([game[0],game[1]])
                    while os.path.exists(directory):
                        directory+="0"
                    print "download ...  url={}  title={}".format(src,text)
                    get_text_and_gif(url=src, save_path_director=directory, class_structure=".quote-content")
                    print "finished url={}".format(src)
                except:
                    print "failed..."
                finally:
                    break



