#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys, re, os, time
import numpy as np
import codecs
import random
from pypinyin import pinyin, lazy_pinyin
from collections import defaultdict

reload(sys)
sys.setdefaultencoding('utf-8')


class GenerateText():
    def __init__(self, country1, country2):
        self.patt_time = re.compile(u"\d+?分钟")
        self.patt_picture = re.compile(u".+?picture")
        self.country1 = "".join(lazy_pinyin(country1))
        self.country2 = "".join(lazy_pinyin(country2))
        self.directory = ["sohu", "eastsport", "hupu"]
        self.getDerectory()

    def getDerectory(self):
        # 获得所有文件路径
        self.director_list = []
        for line in self.directory:
            path = os.listdir(line)
            for p in path:
                paths = line + "/" + p + "/"
                self.director_list.append(paths)

    def judgeOK(self, judge_path):
        # 判断出现\d分钟的次数进行筛选，是否符合选取原始文件
        fp_r = codecs.open(judge_path, 'r', encoding="utf-8")
        count = 0
        for line in fp_r.readlines():
            if re.search(self.patt_time, line.strip().decode("utf-8")):
                count += 1
        fp_r.close()
        if count > 5:
            return True
        else:
            return False

    def getOrigionText(self):
        # 选择需要修改的原始文件，基于此文件进行生成
        # reture：选中的原始文件路径
        restult = []
        for path in self.director_list:
            if self.country1 in path and self.country2 in path:  # and self.judgeOK(os.path.join(path,"text")):
                restult.append(path)
        if not restult:
            raise RuntimeError("原始文件未找到")
        return random.choice(restult)

    def unpackText(self, path):
        result = dict()
        fp_r = codecs.open(path, 'r', encoding="utf-8")
        # 存储文章内容
        tmp = []
        for line in fp_r.readlines():
            tmp.append(line.strip().decode("utf8"))
        fp_r.close()
        lenght = len(tmp)
        text = ""
        minute = ""
        for num in range(0, lenght - 1, 1):
            if self.patt_time.search(tmp[num]) and self.patt_picture.search(tmp[num + 1]):
                text = text + tmp[num] + "\n" + "".join(lazy_pinyin(tmp[num + 1]))
            elif self.patt_picture.search(tmp[num]) and self.patt_picture.search(tmp[num + 1]):
                text = text + "\n" + "".join(lazy_pinyin(tmp[num + 1]))
            elif self.patt_picture.search(tmp[num]) and not self.patt_picture.search(tmp[num + 1]):
                minute_tmp = self.patt_time.findall(text)
                if not minute_tmp:
                    continue
                result[minute_tmp[-1]] = text
                text, minute = "", ""
        return result

    def getFinalDict(self):
        # 得到组合起来{时间：[text,gif1,gif2,...]}总词典
        result = defaultdict(list)
        for line in self.director_list:
            if self.country1 in line and self.country2 in line:
                for key, value in self.unpackText(line + "/text").items():
                    result[key].append(value)
        return result

    def getChartRobotLong(self):
        final_dict = self.getFinalDict()
        orgion_text_path = self.getOrigionText()
        fp_w = open("generate/text", 'w')
        fp_r = codecs.open(orgion_text_path + "/text", 'r', encoding="utf-8")
        text_origion = []
        for lines in fp_r.readlines():
            line = lines.strip().decode("utf-8")
            text_origion.append(line)
        lenght = len(text_origion)
        head = ""
        tail = []
        for num in range(0, lenght, 1):
            if not self.patt_time.search(text_origion[num]):
                head = head + text_origion[num] + "\n"
            else:
                break
        for num2 in range(lenght - 1, 0, -1):
            if not self.patt_time.search(text_origion[num2]):
                tail.append(text_origion[num2])
            else:
                break
        tail = "\n".join(list(reversed(tail)))
        patt_time_tmp = re.compile(u"\d+")
        keys = map(lambda x: int(patt_time_tmp.findall(x)[0]), list(final_dict.keys()))
        keys.sort()
        # save data
        fp_w.write(head)
        for minute in keys:
            text = random.choice(final_dict[str(minute) + u"分钟"])
            fp_w.write(text + "\n")
        fp_w.write(tail)

    def getChartRobot(self):
        final_dict = self.getFinalDict()
        orgion_text_path = self.getOrigionText()
        print "orgion_text_path",orgion_text_path
        fp_w = open("generate/text", 'w')
        fp_r = codecs.open(orgion_text_path + "/text", 'r', encoding="utf-8")
        text_origion = []
        for lines in fp_r.readlines():
            line = lines.strip().decode("utf-8")
            text_origion.append(line)
        fp_r.close()
        lenght = len(text_origion)
        for num in range(0, lenght, 1):
            # 不符合上面两个正则的直接输出内容
            if not self.patt_time.search(text_origion[num]) and not self.patt_picture.search(text_origion[num]):
                print >>fp_w, text_origion[num]
            # 符合时间正则的，两种情况：有替换的就随机替换，没有替换的就直接输出
            elif self.patt_time.search(text_origion[num]):
                minute_patt = self.patt_time.findall(text_origion[num])[-1]
                if final_dict.has_key(minute_patt):
                    text_tmp =random.choice(final_dict[minute_patt])
                    fp_w.write(text_tmp+"\n")
                else:
                    fp_w.write(text_origion[num])
                    if self.patt_picture.search(text_origion[num+1]):
                        fp_w.write(self.patt_picture.findall(text_origion[num+1])[-1]+"\n")
            else:
                pass
               

if __name__ == '__main__':
    gene = GenerateText(u"比利时", u'日本')
    gene.getChartRobotLong()
    #gene.getChartRobot()
