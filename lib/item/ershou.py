#!/usr/bin/env python
# coding=utf-8
# author: zengyuetian
# 此代码仅供学习与交流，请勿用于商业用途。
# 二手房信息的数据结构
import re

class ErShou(object):
    excel_title =  "日期," + \
                "区," + \
                "镇," + \
                "房屋描述," + \
                "单价(元/平)," + \
                "总价(万)," + \
                "地址," + \
                "户型," + \
                "面积(平米)," + \
                "朝向," + \
                "装修," + \
                "楼层," + \
                "建成年份," + \
                "结构," + \
                "图片" + "\n"

    def __init__(self, date, district, area, title, unit_price, total_price, position, desc, pic_url):
        self.date = date
        self.district = district
        self.area = area
        self.title = title
        self.unit_price = unit_price
        self.total_price = total_price
        self.position = position
        self.pic_url = pic_url
        self.desc = desc
        self.huxing = "未知"
        self.mianji = "未知"
        self.chaoxiang = "未知"
        self.zhuangxiu = "未知"
        self.floor = "未知"
        self.built_year = "未知"
        self.struct = "未知"

    def set_value(self, date, district, area, title,
                  unit_price, total_price, position, huxing,
                  mianji, chaoxiang, zhuangxiu, floor,
                  built_year, struct, pic_url):
        self.date  = date
        self.district  = district
        self.area  = area
        self.title  = title
        self.unit_price  = unit_price
        self.total_price  = total_price
        self.position  = position
        self.huxing  = huxing
        self.mianji  = mianji
        self.chaoxiang  = chaoxiang
        self.zhuangxiu  = zhuangxiu
        self.floor  = floor
        self.built_year  = built_year
        self.struct  = struct
        self.pic_url = pic_url

    def desc_handler(self):
        #['1室1厅 ', ' 35.8平米 ', ' 南 ', ' 毛坯 ', ' 低楼层(共6层) ', ' 1996年建 ', ' 板楼']
        desc_list = self.desc.split(sep="|")
        num = len(desc_list)
        if num >=7:
            self.huxing = desc_list[0].strip()
            self.mianji = desc_list[1].strip().replace("平米", "")
            self.chaoxiang = desc_list[2].strip()
            self.zhuangxiu = desc_list[3].strip()
            self.floor = desc_list[4].strip()
            self.built_year = desc_list[5].strip().replace("年建", "")
            if num == 7:
                self.struct = desc_list[6].strip()
            else:
                self.struct = desc_list[6].strip() + desc_list[7].strip()
        else:
            hx_pat = re.compile('\d{1,2}室\d{1,2}厅')
            cx_pat = re.compile('[东西南北]')
            by_pat = re.compile('年建')
            fl_pat = re.compile('层')
            zx_pat = re.compile('[精装简毛坯]')
            st_pat = re.compile('[塔楼板]')

            for i in range(0, num):
                txt = desc_list[i].strip()

                huxing = hx_pat.search(txt)
                chaoxiang = cx_pat.search(txt)
                builtyear = by_pat.search(txt)
                floor = fl_pat.search(txt)
                zhuangxiu = zx_pat.search(txt)
                struct = st_pat.search(txt)

                if huxing is not None:
                    self.huxing = txt
                elif chaoxiang is not None:
                    self.chaoxiang = txt
                elif builtyear is not None:
                    self.built_year = txt.replace("年建", "")
                elif floor is not None:
                    self.floor = txt
                elif zhuangxiu is not None:
                    self.zhuangxiu = txt
                elif struct is not None:
                    self.struct = txt
                elif "平米" in txt:
                    self.mianji = txt.replace("平米", "")

    def text(self):
        self.desc_handler()

        return self.date + "," + \
                self.district + "," + \
                self.area + "," + \
                self.title + "," + \
                self.unit_price + "," + \
                self.total_price + "," + \
                self.position + "," + \
                self.huxing + "," + \
                self.mianji + "," + \
                self.chaoxiang + "," + \
                self.zhuangxiu + "," + \
                self.floor + "," + \
                self.built_year + "," + \
                self.struct + "," + \
                self.pic_url + "\n"
