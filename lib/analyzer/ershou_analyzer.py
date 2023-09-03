import os
import sys
import numpy as np

if __name__ != "__main__":
    from lib.zone.district import *


class ErShouAnalyzer(object):
    def __init__(self):
        self.district_areas_house_info_dict = dict()

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

    def data_analyzer(self):
        for k, v in self.district_areas_house_info_dict.items():
            if type(v) is dict:
                for k1, v1 in v.items():
                    if len(v1) > 0 and type(v1) is list:
                        print(v1[0])

if __name__ == "__main__":
    lib_path=os.path.dirname(sys.path[0])
    root_path = os.path.dirname(lib_path)
    sys.path.append(root_path)

    from lib.utility import path
    from lib.spider.base_spider import SPIDER_NAME
    from lib.zone.area import *
    import csv

    city = 'sh'
    districts_pinyin_names = get_districts(city)
    for district_pinyin_name in districts_pinyin_names:
        area_pinyin_names_of_district = get_areas(city, district_pinyin_name)

    csv_path = path.DATA_PATH + "/" + SPIDER_NAME + "/ershou/" + "sh/20230828"
    print("csv data path: ", csv_path)

    csv_lists = os.listdir(csv_path)

    ershou_analyzer = ErShouAnalyzer()
    for csv_file in csv_lists:
        district_pinyin_name, area_pinyin_name = csv_file.replace(".csv", '').split(sep='_')

        with open(csv_path + "/" + csv_file, encoding='utf-8') as f:
            ershou_houses_list = list(csv.reader(f, skipinitialspace=True))
            ershou_analyzer.add_area_houses_info_to_dict(district_pinyin_name,
                                                         area_pinyin_name,
                                                         ershou_houses_list)

    ershou_analyzer.data_analyzer()
