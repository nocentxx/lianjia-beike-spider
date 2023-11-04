#!/usr/bin/env python
# coding=utf-8
# author: zengyuetian
# 此代码仅供学习与交流，请勿用于商业用途。
# 城市缩写和城市名的映射
# 想抓取其他已有城市的话，需要把相关城市信息放入下面的字典中
# 不过暂时只有下面这些城市在链家上是统一样式

import os
import random
import re
import requests
import sys

from bs4 import BeautifulSoup

if __name__ != "__main__":
    from lib.utility.version import PYTHON_3
    from lib.utility.log import *

cities = dict()
#cities = {
#    'bj': '北京',
#    'cd': '成都',
#    'cq': '重庆',
#    'cs': '长沙',
#    'dg': '东莞',
#    'dl': '大连',
#    'fs': '佛山',
#    'gz': '广州',
#    'hz': '杭州',
#    'hf': '合肥',
#    'jn': '济南',
#    'nj': '南京',
#    'qd': '青岛',
#    'sh': '上海',
#    'sz': '深圳',
#    'su': '苏州',
#    'sy': '沈阳',
#    'tj': '天津',
#    'wh': '武汉',
#    'xm': '厦门',
#    'yt': '烟台',
#}


lianjia_cities = cities
beike_cities = cities

USER_AGENTS = [
    "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; AcooBrowser; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0; Acoo Browser; SLCC1; .NET CLR 2.0.50727; Media Center PC 5.0; .NET CLR 3.0.04506)",
    "Mozilla/4.0 (compatible; MSIE 7.0; AOL 9.5; AOLBuild 4337.35; Windows NT 5.1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
    "Mozilla/5.0 (Windows; U; MSIE 9.0; Windows NT 9.0; en-US)",
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 2.0.50727; Media Center PC 6.0)",
    "Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 1.0.3705; .NET CLR 1.1.4322)",
    "Mozilla/4.0 (compatible; MSIE 7.0b; Windows NT 5.2; .NET CLR 1.1.4322; .NET CLR 2.0.50727; InfoPath.2; .NET CLR 3.0.04506.30)",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN) AppleWebKit/523.15 (KHTML, like Gecko, Safari/419.3) Arora/0.3 (Change: 287 c9dfb30)",
    "Mozilla/5.0 (X11; U; Linux; en-US) AppleWebKit/527+ (KHTML, like Gecko, Safari/419.3) Arora/0.6",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.2pre) Gecko/20070215 K-Ninja/2.1.1",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9) Gecko/20080705 Firefox/3.0 Kapiko/3.0",
    "Mozilla/5.0 (X11; Linux i686; U;) Gecko/20070322 Kazehakase/0.4.5",
    "Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.8) Gecko Fedora/1.9.0.8-1.fc10 Kazehakase/0.5.6",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_3) AppleWebKit/535.20 (KHTML, like Gecko) Chrome/19.0.1036.7 Safari/535.20",
    "Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; fr) Presto/2.9.168 Version/11.52",
]


def request_headers():
    headers = dict()
    headers["User-Agent"] = random.choice(USER_AGENTS)
    headers["Referer"] = "http://www.{0}.com".format('lianjia')
    return headers

def crawl_cities():
    city_url = 'https://www.lianjia.com/city/'
    print(city_url)

    headers = request_headers()
    response = requests.get(city_url, timeout=50, headers=headers)

    html = response.content
    soup = BeautifulSoup(html, "lxml")

    div_class = 'city_province'
    province_list = soup.find_all('div', class_=div_class)

    for province_item in province_list:
        #<div class="city_province">
        #<i></i>
        #<div class="city_list_tit c_b">云南</div>
        #<ul>
        #<li><a href="https://dali.lianjia.com/">大理</a></li>
        #<li><a href="https://km.lianjia.com/">昆明</a></li>
        #<li><a href="https://xsbn.lianjia.com/">西双版纳</a></li>
        #</ul>
        #</div>
        province = province_item.find('div', class_='city_list_tit c_b')
        province_name = province.text
        logger.info(province_name)

        city_list = province_item.find_all('a')

        pattern = re.compile('(fang)|(you).lianjia.com/')

        for city_item in city_list:
            city_name = city_item.text
            abbr_url = city_item.get('href')
            ret = pattern.search(abbr_url)
            if ret is not None:
                print("ignore city: ", city_name, abbr_url)
                continue
            else:
                city_abbr = re.sub('http.*://', '', abbr_url).replace('.lianjia.com/', '')

            cities[city_abbr] = city_name

            logger.info(city_abbr)
            logger.info(city_name)


def create_prompt_text():
    """
    根据已有城市中英文对照表拼接选择提示信息
    :return: 拼接好的字串
    """
    crawl_cities()
    city_info = list()
    count = 0
    for en_name, ch_name in cities.items():
        count += 1
        city_info.append(en_name)
        city_info.append(": ")
        city_info.append(ch_name)
        if count % 4 == 0:
            city_info.append("\n")
        else:
            city_info.append(", ")
    return 'Which city do you want to crawl?\n' + ''.join(city_info)


def get_city_cn_name(city_pinyin_name):
    """
    拼音拼音名转中文城市名
    :param en: 拼音
    :return: 中文
    """
    return cities.get(city_pinyin_name, None)


def get_city():
    city = None
    # 允许用户通过命令直接指定
    if len(sys.argv) < 2:
        print("Wait for your choice.")
        # 让用户选择爬取哪个城市的二手房小区价格数据
        prompt = create_prompt_text() + "\n"
        # 判断Python版本
        if not PYTHON_3:  # 如果小于Python3
            city = raw_input(prompt)
        else:
            city = input(prompt)
    elif len(sys.argv) == 2:
        city = str(sys.argv[1])
        print("City is: {0}".format(city))
    else:
        print("At most accept one parameter.")
        exit(1)

    city_cn_name = get_city_cn_name(city)
    if city_cn_name is not None:
        message = 'OK, start to crawl ' + get_city_cn_name(city)
        print(message)
        logger.info(message)
    else:
        print("No such city, please check your input.")
        exit(1)
    return city


if __name__ == '__main__':
    lib_path=os.path.dirname(sys.path[0])
    root_path = os.path.dirname(lib_path)
    sys.path.append(root_path)

    from lib.utility.version import PYTHON_3
    from lib.utility.log import *

    print(crawl_cities())
    #print(get_city_cn_name("sh"))
