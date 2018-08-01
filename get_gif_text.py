#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
import requests
from bs4 import BeautifulSoup
import sys
import urllib
import urllib2
import time
import shutil
import re,os
from pypinyin import pinyin, lazy_pinyin

reload(sys)
sys.setdefaultencoding('utf8')

'''
先下载gif图和text
'''
def get_html(url):
    response = requests.get(url=url)
    text = response.text
    sout = BeautifulSoup(text, 'lxml')
    return sout


def get_text_and_gif(url, save_path_director,class_structure):
    result_list = []
    sout = get_html(url=url)
    texts = sout.select(str(class_structure))
    pattern_gif = re.compile("http.+?gif")
    pattern_text = re.compile("<.+?>")
    for text in texts:
        for line in text:
            line_string = str(line)
            if re.search(pattern_gif, line_string):
                find_gif = re.findall(pattern_gif, line_string)
                if find_gif:
                    result_list.extend(list(set(find_gif)))
            else:
                find_text = re.sub(pattern_text, "", line_string)
                if find_text:
                    result_list.extend([find_text])
    # 不包含gif图，跳过下载
    if '.gif' in "".join(result_list):
        if os.path.exists(save_path_director):
            shutil.rmtree(save_path_director)
        if not save_path_director.endswith("/"):
            save_path_director = save_path_director + "/"
        save_path_director = "".join(lazy_pinyin(unicode(save_path_director)))
        os.makedirs(save_path_director)
        fp_w_text = open(os.path.join(save_path_director, "text"), 'w')
        fp_w_url = open(os.path.join(save_path_director, "url"), 'w')
        print >>fp_w_url,url
        file_count = 0
        filters=[u'虎扑',u'搜狐',u'东方体育']
        for num,line1 in enumerate(result_list):
            # 来源替换
            li=str(line1).strip().replace(u'虎扑','新浪网').replace(u'搜狐','新浪网').replace(u'东方体育','新浪网')
            li=re.sub(re.compile('\[.+?\]'),'',li)
            if li=="":
                continue
            #gif图片和text按照文中顺序存储
            if re.search(pattern_gif, li):
                fp_w_gif = save_path_director + u"picture" + str(file_count) + u".gif"
                urllib.urlretrieve(li.encode("utf-8"), fp_w_gif)
                print >>fp_w_text,fp_w_gif
                file_count += 1
            else:
                print >>fp_w_text,li.decode('utf-8')

if __name__ == '__main__':
    url = "https://www.sohu.com/a/239135093_461392"
    path = "sohu/瑞典-瑞士"
    try:
        os.makedirs(path)
    except:
        pass
    get_text_and_gif(url,path,".article")
