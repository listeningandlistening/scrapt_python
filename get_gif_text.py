#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
import requests

if __name__ == '__main__':
    url = "https://www.sohu.com/a/239135093_461392"
    path = "sohu/瑞典-瑞士"
    try:
        os.makedirs(path)
    except:
        pass
    get_text_and_gif(url,path,".article")
