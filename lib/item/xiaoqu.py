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


class DealFrame(object):
    deal_frame_title = "交易日期,面积,价格,单价,描述,小区,交易权属,建成年代,均价,建筑类型,房屋总数,楼栋总数,绿化率,容积率,用水类型,用电类型,供暖类型,地铁,物业费,物业公司,开发商,中介\n"

    def __init__(self, dealDate, dealArea, dealPrice, dealUnitPrice, dealDesc, detailTitle,
                 trade_type, built_year, aver_price, building_type,
                 house_total, building_total, greening_ratio, plot_ratio,
                 water_type, elec_type, heating_type, subway_info,
                 property_fee, property_company, real_estate, intermediary):
        self.dealDate = dealDate
        self.dealArea = dealArea
        self.dealPrice = dealPrice
        self.dealUnitPrice = dealUnitPrice
        self.dealDesc = dealDesc
        self.detailTitle = detailTitle
        self.trade_type = trade_type
        self.built_year = built_year
        self.aver_price = aver_price
        self.building_type = building_type
        self.house_total = house_total
        self.building_total = building_total
        self.greening_ratio = greening_ratio
        self.plot_ratio = plot_ratio
        self.water_type = water_type
        self.elec_type = elec_type
        self.heating_type = heating_type
        self.subway_info = subway_info
        self.property_fee = property_fee
        self.property_company = property_company
        self.real_estate = real_estate
        self.intermediary = intermediary

    def text(self):
        return self.dealDate + "," + \
        self.dealArea + "," + \
        self.dealPrice + "," + \
        self.dealUnitPrice + "," + \
        self.dealDesc + "," + \
        self.detailTitle + "," + \
        self.trade_type + "," + \
        self.built_year + "," + \
        self.building_type + "," + \
        self.house_total + "," + \
        self.building_total + "," + \
        self.greening_ratio + "," + \
        self.plot_ratio + "," + \
        self.water_type + "," + \
        self.elec_type + "," + \
        self.heating_type + "," + \
        self.subway_info + "," + \
        self.property_fee + "," + \
        self.property_company + "," + \
        self.real_estate + "," + \
        self.intermediary + "\n"
