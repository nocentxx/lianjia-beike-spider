#!/usr/bin/env python
# coding=utf-8
# author: zengyuetian
# 此代码仅供学习与交流，请勿用于商业用途。
# 二手房信息的数据结构


class ErShou(object):
    def __init__(self, district, area, title, unit_price, total_price, position, desc, pic_url):
        self.district = district
        self.area = area
        self.title = title
        self.unit_price = unit_price
        self.total_price = total_price
        self.position = position
        self.desc = desc
        self.pic_url = pic_url

    def text(self):
        return self.district + "," + \
                self.area + "," + \
                self.title + "," + \
                self.unit_price + "," + \
                self.total_price + "," + \
                self.position + "," + \
                self.desc + "," + \
                self.pic_url + "\n"
