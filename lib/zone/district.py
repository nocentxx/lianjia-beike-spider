#!/usr/bin/env python
# coding=utf-8
# author: zengyuetian
# 此代码仅供学习与交流，请勿用于商业用途。
# 获得各城市的区县相关信息

import requests
from lxml import etree
from lib.zone.city import cities
from lib.const.xpath import *
from lib.request.headers import *
from lib.spider.base_spider import SPIDER_NAME

district_pinyin_cn_name_dict = dict()     # 城市代码和中文名映射
area_pinyin_cn_name_dict = dict()              # 版块代码和中文名映射
area_district_pinyin_name_dict = dict()


def get_district_cn_name(en):
    """
    拼音区县名转中文区县名
    :param en: 英文
    :return: 中文
    """
    return district_pinyin_cn_name_dict.get(en, None)


def get_districts(city):
    """
    获取各城市的区县中英文对照信息
    :param city: 城市
    :return: 英文区县名列表
    """
    url = 'https://{0}.{1}.com/ershoufang/'.format(city, SPIDER_NAME)
    headers = create_headers()
    response = requests.get(url, timeout=10, headers=headers)
    html = response.content
    root = etree.HTML(html)
    elements = root.xpath(CITY_DISTRICT_XPATH)

    pinyin_names = list()
    ch_names = list()
    for element in elements:
        link = element.attrib['href']
        pinyin_names.append(link.split('/')[-2])
        ch_names.append(element.text)

        # 打印区县英文和中文名列表
    for index, pinyin_name in enumerate(pinyin_names):
        district_pinyin_cn_name_dict[pinyin_name] = ch_names[index]
    print(district_pinyin_cn_name_dict)
    return pinyin_names


if __name__ == '__main__':
    for key in cities.keys():
        # 寻找那些网页格式不合规的城市
        district_pinyin_cn_name_dict = dict()
        get_districts(key)
        if len(district_pinyin_cn_name_dict.items()) == 0:
            print(key)
