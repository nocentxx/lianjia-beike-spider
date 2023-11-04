import os
import sys
import numpy as np

if __name__ != "__main__":
    from lib.zone.district import *
    from lib.item.ershou import *

class AreaErShou(object):
    summary_title =  "日期," + \
        "区," + \
        "镇," + \
        "数量," + \
        "单价平均(元/平)," + \
        "总价平均(万)," + \
        "面积平均(平米)," + \
        "建成年份平均\n"
    def __init__(self, date, district, area, quantity, unit_price_avrg, total_price_avrg, mianji_avrg, by_avrg):
        self.date = date
        self.district = district
        self.area = area
        self.quantity = quantity
        self.up_avrg = unit_price_avrg # unit_price_avrg
        self.tp_avrg = total_price_avrg # total_price_avrg
        self.mianji_avrg = mianji_avrg
        self.by_avrg = by_avrg # built_year_avrg

    def text(self):
        return self.date + "," + \
            self.district + "," + \
            self.area + "," + \
            str(self.quantity) + "," + \
            str(self.up_avrg) + "," + \
            str(self.tp_avrg) + "," + \
            str(self.mianji_avrg) + "," + \
            str(self.by_avrg) + "\n"


class ErShouAnalyzer(object):
    def __init__(self):
        self.city_pinyin_name = None
        self.summary_path = None
        self.district_areas_house_info_dict = dict()
        self.summary_list = list()

    def set_base_info(self, city_pinyin_name, summary_path):
        self.city_pinyin_name = city_pinyin_name
        self.summary_path = summary_path

    def add_area_houses_info_to_dict(self,
                                     district_pinyin_name,
                                     area_pinyin_name,
                                     ershou_houses_list):
        if self.district_areas_house_info_dict.get(district_pinyin_name) is None:
            self.district_areas_house_info_dict[district_pinyin_name] = dict()

        area_houses_dict = self.district_areas_house_info_dict[district_pinyin_name]
        area_houses_dict[area_pinyin_name] = ershou_houses_list

        try:
            print("add {0} {1} houses to {2}".format(
                area_pinyin_cn_name_dict[area_pinyin_name],
                len(ershou_houses_list),
                district_pinyin_cn_name_dict[district_pinyin_name]))
        except Exception as e:
            print("error: ", e)

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
        return AreaErShou(ershous_list[0].date, ershous_list[0].district, ershous_list[0].area, unit_price_num, average_up, average_tp, average_mj, average_by)

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

        for summary_item in self.summary_list:
            summary_item_sum += 1
            quantity_sum += summary_item.quantity
            up_avrg_sum += summary_item.up_avrg
            tp_avrg_sum += summary_item.tp_avrg
            mj_avrg_sum += summary_item.mianji_avrg
            by_avrg_sum += summary_item.by_avrg

            # district scope summary
            area_csv_file = self.summary_path + "/{0}_{1}_summary.csv".format(summary_item.district, summary_item.area)
            print(area_csv_file)

            if not os.path.isfile(area_csv_file):
                with open(area_csv_file, "w") as f:
                    f.write(AreaErShou.summary_title) # write first row(title) of csv file

            with open(area_csv_file, "a") as f:
                f.write(summary_item.text())

        # city scope summary
        csv_file = self.summary_path + "/{0}_summary.csv".format(self.city_pinyin_name)
        print(csv_file)
        if not os.path.isfile(csv_file):
            with open(csv_file, "w") as f:
                f.write(AreaErShou.summary_title) # write first row(title) of csv file

        with open(csv_file, "a") as f:
            up_avrg_sum_avrg = up_avrg_sum/summary_item_sum
            tp_avrg_sum_avrg = tp_avrg_sum/summary_item_sum
            mj_avrg_sum_avrg = mj_avrg_sum/summary_item_sum
            by_avrg_sum_avrg = by_avrg_sum/summary_item_sum

            f.write(self.summary_list[0].date + "," + self.city_pinyin_name + ",N/A," + \
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
    from lib.item.ershou import *
    import csv

    def csv_item_to_ershou_item_list(csv_item_list):
        ershou_list = list()

        for i in range(1, len(csv_item_list)):
            try:
                ershou_item = csv_item_list[i]
                # 作为对象保存
                ershou = ErShou(ershou_item[0], ershou_item[1], ershou_item[2], ershou_item[3],
                            ershou_item[4], ershou_item[5], ershou_item[6], ershou_item[7],
                            ershou_item[8])

                ershou.set_value(ershou_item[0], ershou_item[1], ershou_item[2], ershou_item[3],
                            ershou_item[4], ershou_item[5], ershou_item[6], ershou_item[7],
                            ershou_item[8], ershou_item[9], ershou_item[10], ershou_item[11],
                            ershou_item[12], ershou_item[13], ershou_item[14])

                ershou_list.append(ershou)
            except Exception as e:
                print("current item: ", ershou_item)

        return ershou_list

    city_pinyin_name = 'sh'
    districts_pinyin_names = get_districts(city_pinyin_name)
    for district_pinyin_name in districts_pinyin_names:
        area_pinyin_names_of_district = get_areas(city_pinyin_name, district_pinyin_name)

    today_path = path.DATA_PATH + "/" + SPIDER_NAME + "/ershou/" + city_pinyin_name + "/20231104"
    summary_path = path.create_summary_path("{0}/ershou".format(SPIDER_NAME), city_pinyin_name)
    print("today_path: ", today_path)

    csv_lists = os.listdir(today_path)

    ershou_analyzer = ErShouAnalyzer()
    ershou_analyzer.set_base_info(city_pinyin_name, summary_path)
    for csv_file in csv_lists:
        if csv_file == city_pinyin_name + "_summary.csv":
            continue

        district_pinyin_name, area_pinyin_name = csv_file.replace(".csv", '').split(sep='_')

        with open(today_path + "/" + csv_file, encoding='utf-8') as f:
            csv_item_list = list(csv.reader(f, skipinitialspace=True))
            ershou_houses_list = csv_item_to_ershou_item_list(csv_item_list)
            ershou_analyzer.add_area_houses_info_to_dict(district_pinyin_name,
                                                         area_pinyin_name,
                                                         ershou_houses_list)

    ershou_analyzer.data_analyzer()
