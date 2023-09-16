#!/usr/bin/env python
# coding=utf-8
# author: zengyuetian
# 此代码仅供学习与交流，请勿用于商业用途。
# 小区信息的数据结构


class XiaoQu(object):
    xiaoqu_title = "日期,区,县,小区,建造年份,均价,在售数量,90天成交数量,在租数量,地铁信息\n"

    def __init__(self, district, area, xq_name, built_year, price, on_sale_count,
                 deal_count_of_90days, on_rent_count, subway_info):
        self.district = district
        self.area = area
        self.xq_name = xq_name
        self.built_year = built_year
        self.price = price
        self.on_sale_count = on_sale_count
        self.deal_count_of_90days = deal_count_of_90days
        self.on_rent_count = on_rent_count
        self.subway_info = subway_info

    def text(self):
        return self.district + "," + \
                self.area + "," + \
                self.xq_name + "," + \
                self.built_year + "," + \
                self.price + "," + \
                self.on_sale_count + "," + \
                self.deal_count_of_90days + "," + \
                self.on_rent_count + "," + \
                self.subway_info + '\n'
