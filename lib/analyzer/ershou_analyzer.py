import os
import sys
import numpy as np

if __name__ != "__main__":
    from lib.zone.district import *

class AreaErShou(object):
    summary_title =  "日期," + \
        "区," + \
        "镇," + \
        "数量," + \
        "单价平均(元/平)," + \
        "总价平均(万)," + \
        "面积平均(平米)," + \
        "建成年份平均\n"
    def __init__(self, date, distrcit, area, quantity, unit_price_avrg, total_price_avrg, mianji_avrg, by_avrg):
        self.date = date
        self.distrcit = distrcit
        self.area = area
        self.quantity = quantity
        self.up_avrg = unit_price_avrg # unit_price_avrg
        self.tp_avrg = total_price_avrg # total_price_avrg
        self.mianji_avrg = mianji_avrg
        self.by_avrg = by_avrg # built_year_avrg

    def text(self):
        return self.date + "," + \
            self.distrcit + "," + \
            self.area + "," + \
            str(self.quantity) + "," + \
            str(self.up_avrg) + "," + \
            str(self.tp_avrg) + "," + \
            str(self.mianji_avrg) + "," + \
            str(self.by_avrg) + "\n"


class ErShouAnalyzer(object):
    def __init__(self):
        if __name__ != "__main__":
            self.city_pinyin_name = None
        else:
            self.city_pinyin_name = "sh"

        self.today_path = None
        self.district_areas_house_info_dict = dict()
        self.summary_list = list()

    def set_base_info(self, today_path, city_pinyin_name):
        self.city_pinyin_name = city_pinyin_name
        self.today_path = today_path

    def add_area_houses_info_to_dict(self,
                                     district_pinyin_name,
                                     area_pinyin_name,
                                     ershou_houses_list):
        if self.district_areas_house_info_dict.get(district_pinyin_name) is None:
            self.district_areas_house_info_dict[district_pinyin_name] = dict()

        area_houses_dict = self.district_areas_house_info_dict[district_pinyin_name]
        area_houses_dict[area_pinyin_name] = ershou_houses_list

        print("add {0} {1} houses to {2}".format(
            area_pinyin_cn_name_dict[area_pinyin_name],
            len(ershou_houses_list),
            district_pinyin_cn_name_dict[district_pinyin_name]))

    def average_calculator(self, ershous_list):
        unit_price = 0
        unit_price_num = 0
        total_price = 0
        total_price_num = 0
        mianji = 0
        mianji_num = 0
        year = 0
        year_num = 0

        for i in range(1, len(ershous_list)):
            ershou_item = ershous_list[i]
            if __name__ != "__main__":
                try:
                    unit_price += float(ershou_item.unit_price)
                    unit_price_num += 1
                except ValueError as e:
                    print(f"unit_price conversion: {e}")

                try:
                    total_price += float(ershou_item.total_price)
                    total_price_num +=1
                except ValueError as e:
                    print(f"tatal_price conversion: {e}")

                try:
                    mianji += float(ershou_item.mianji)
                    mianji_num +=1
                except ValueError as e:
                    print(f"mianji conversion: {e}")

                try:
                    year += float(ershou_item.built_year)
                    year_num +=1
                except ValueError as e:
                    print(f"built_year conversion: {e}")
            else:
                try:
                    unit_price += float(ershou_item[4])
                    unit_price_num += 1
                except ValueError as e:
                    print(f"unit_price conversion: {e}")

                try:
                    total_price += float(ershou_item[5])
                    total_price_num +=1
                except ValueError as e:
                    print(f"tatal_price conversion: {e}")

                try:
                    mianji += float(ershou_item[8])
                    mianji_num +=1
                except ValueError as e:
                    print(f"mianji conversion: {e}")

                try:
                    year += float(ershou_item[12])
                    year_num +=1
                except ValueError as e:
                    print(f"built_year conversion: {e}")

        average_up = 0
        average_tp = 0
        average_mj = 0
        average_by = 0

        if unit_price_num != 0:
            average_up = unit_price/unit_price_num
        if total_price_num != 0:
            average_tp = total_price/total_price_num
        if mianji_num != 0:
            average_mj = mianji/mianji_num
        if year_num != 0:
            average_by = year/year_num

        print("average: ", average_up, average_tp, average_mj, average_by)
        if __name__ != "__main__":
            return AreaErShou(ershou_item.date, ershou_item.district, ershou_item.area, unit_price_num, average_up, average_tp, average_mj, average_by)
        else:
            return AreaErShou(ershou_item[0], ershou_item[1], ershou_item[2], unit_price_num, average_up, average_tp, average_mj, average_by)

    def data_analyzer(self):
        for k, v in self.district_areas_house_info_dict.items():
            if type(v) is dict:
                for k1, v1 in v.items():
                    if len(v1) > 0 and type(v1) is list:
                        average_info = self.average_calculator(v1)
                        self.summary_list.append(average_info)

        self.write_summary()

    def write_summary(self, fmt="csv"):
        summary_item_sum = 0
        quantity_sum = 0
        up_avrg_sum = 0
        tp_avrg_sum = 0
        mj_avrg_sum = 0
        by_avrg_sum = 0

        csv_file = self.today_path + "/{0}_summary.csv".format(self.city_pinyin_name)
        print(csv_file)

        with open(csv_file, "w") as f:
            f.write(AreaErShou.summary_title) # write first row(title) of csv file
            for summary_item in self.summary_list:
                f.write(summary_item.text())

                summary_item_sum += 1
                quantity_sum += summary_item.quantity
                up_avrg_sum += summary_item.up_avrg
                tp_avrg_sum += summary_item.tp_avrg
                mj_avrg_sum += summary_item.mianji_avrg
                by_avrg_sum += summary_item.by_avrg

            up_avrg_sum_avrg = up_avrg_sum/summary_item_sum
            tp_avrg_sum_avrg = tp_avrg_sum/summary_item_sum
            mj_avrg_sum_avrg = mj_avrg_sum/summary_item_sum
            by_avrg_sum_avrg = by_avrg_sum/summary_item_sum

            f.write("N/A," + self.city_pinyin_name + ",N/A," + \
                    str(quantity_sum) + "," + \
                    str(up_avrg_sum_avrg) + "," + \
                    str(tp_avrg_sum_avrg) + "," + \
                    str(mj_avrg_sum_avrg) + "," + \
                    str(by_avrg_sum_avrg) + "\n")


if __name__ == "__main__":
    lib_path=os.path.dirname(sys.path[0])
    root_path = os.path.dirname(lib_path)
    sys.path.append(root_path)

    from lib.utility import path
    from lib.spider.base_spider import SPIDER_NAME
    from lib.zone.area import *
    import csv

    city_pinyin_name = 'sh'
    districts_pinyin_names = get_districts(city_pinyin_name)
    for district_pinyin_name in districts_pinyin_names:
        area_pinyin_names_of_district = get_areas(city_pinyin_name, district_pinyin_name)

    today_path = path.DATA_PATH + "/" + SPIDER_NAME + "/ershou/" + city_pinyin_name + "/20230916"
    print("today csv data path: ", today_path)

    csv_lists = os.listdir(today_path)

    ershou_analyzer = ErShouAnalyzer()
    ershou_analyzer.set_base_info(today_path, city_pinyin_name)
    for csv_file in csv_lists:
        if csv_file == city_pinyin_name + "_summary.csv":
            continue

        district_pinyin_name, area_pinyin_name = csv_file.replace(".csv", '').split(sep='_')

        with open(today_path + "/" + csv_file, encoding='utf-8') as f:
            ershou_houses_list = list(csv.reader(f, skipinitialspace=True))
            ershou_analyzer.add_area_houses_info_to_dict(district_pinyin_name,
                                                         area_pinyin_name,
                                                         ershou_houses_list)

    ershou_analyzer.data_analyzer()
