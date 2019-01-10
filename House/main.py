# -*- coding: utf-8 -*-
# @Time    : 2019/1/10 19:58
# @Author  : yueconger
# @File    : main.py
import os
import sys
from scrapy.cmdline import execute

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
execute(['scrapy', 'crawl', 'house_nj'])
