#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
import requests
from bs4 import BeautifulSoup
import re
import os
import urllib
import shutil
import time
from pypinyin import pinyin, lazy_pinyin

import sys

def get_html(url):
    response = requests.get(url=url)
    text = response.text.encode('ISO-8859-1')
    sout = BeautifulSoup(text, 'lxml')
    return sout


def get_gif_text(url, save_path_director):
    result_list = []
    url_list = []
    # cu存在翻页情况，存储当前内容所有可能url
    for i in range(0, 10):
        if i == 0:
            url_list.append(url)
        else:
            location = url.rfind(".")
            head, tail = url[:location], url[location:]
            merge_url = head + "-" + str(i) + tail
            url_list.append(merge_url)
    pattern_gif = re.compile("src=\".+?gif")
    pattern_text = re.compile("<.+?>")
    for url_tmp in url_list:
        try:
            sout = get_html(url=url_tmp)
            texts = sout.find_all(class_="txt mt15")[0]
            for text in texts:
                line_string = str(text)
                if re.search(pattern_gif, line_string):
                    find_gif = re.findall(pattern_gif, line_string)
                    if find_gif:
                        tmp=map(lambda x:x.replace("src=\"",""),find_gif)
                        result_list.extend(list(set(tmp)))
                else:
                    find_text = re.sub(pattern_text, "", line_string)
                    find_text = find_text.replace(" ", "").strip()
                    if find_text:
                        result_list.extend([find_text])
        except:
            pass
    if 'gif' in "".join(result_list):
        if os.path.exists(save_path_director):
            shutil.rmtree(save_path_director)
        if not save_path_director.endswith("/"):
            save_path_director = save_path_director + "/"
        save_path_director = "".join(lazy_pinyin(unicode(save_path_director)))
        os.makedirs(save_path_director)
        fp_w_text = open(os.path.join(save_path_director, "text"), 'w')
        fp_w_url = open(os.path.join(save_path_director, "url"), 'w')
        print >> fp_w_url, url
        file_count = 0
        filters = [u'虎扑', u'搜狐', u'东方体育']
        for num, line1 in enumerate(result_list):
            # 来源替换
            li = str(line1).strip().replace(u'虎扑', '新浪网').replace(u'搜狐', '新浪网').replace(u'东方体育', '新浪网')
            li = re.sub(re.compile('\[.+?\]'), '', li)
            if li == "":
                continue
            # gif图片和text按照文中顺序存储
            if ".gif" in li:
                if not "https" in li:
                    li="https:"+li
                fp_w_gif = os.path.join(save_path_director, "picture" + str(file_count) + ".gif")
                urllib.urlretrieve(li, fp_w_gif)
                print >> fp_w_text, fp_w_gif
                file_count += 1
            else:
                print >> fp_w_text, li.decode('utf-8')

def get_target_urls(url):
    result=dict()
    sout=get_html(url)
    content=sout.select('div[class="infor-wrapper clr"]')
    news_content=content[0].select("a")
    for line in news_content:
        src=line.attrs["href"]
        text=line.getText()
        result[src]=text
    return result

if __name__ == '__main__':
    url="https://sports.eastday.com/"
    games = [(u'西班牙', u'俄罗斯'), (u'克罗地亚', u'丹麦'), (u"巴西", u'墨西哥'),(u'比利时',u'日本'),(u'英格兰',u'哥伦比亚'),(u'瑞典',u'瑞士')]
    scores = re.compile(u'(\d)(-|:|：)(\d)')
    scores2 = re.compile(u'场\d+?球')
    score3 = re.compile(u"\d+?强")
    urls_dict = get_target_urls(url)
    print "--" * 40
    for src, text in urls_dict.items():
        flag = False
        for game1, game2 in games:
            if game1 in text and game2 in text:
                flag = True
            if (scores.search(text) or scores2.search(text) or score3.search(text)) and (game1 in text or game2 in text):
                flag = True
            if flag:
                directory = "eastsport/" + "-".join([game1, game2])
                while os.path.exists(directory):
                    directory += "0"
                print "download ...  url={}".format(src)
                get_gif_text(src, directory)
                print "finished url={}".format(src)
                break

