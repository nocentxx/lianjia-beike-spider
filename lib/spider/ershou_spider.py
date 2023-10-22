#!/usr/bin/env python
# coding=utf-8
# author: zengyuetian
# 此代码仅供学习与交流，请勿用于商业用途。
# 爬取二手房数据的爬虫派生类

import re
import threadpool
from bs4 import BeautifulSoup
from lib.analyzer.ershou_analyzer import *
from lib.item.ershou import *
from lib.zone.city import get_city
from lib.spider.base_spider import *
from lib.utility.date import *
from lib.utility.path import *
from lib.zone.area import *
from lib.utility.log import *
import lib.utility.version


class ErShouSpider(BaseSpider):
    def __init__(self, spider_name):
        super(ErShouSpider, self).__init__(spider_name)
        self.ershou_analyzer = ErShouAnalyzer()

    def collect_area_ershou_data(self, city_pinyin_name, area_pinyin_name, fmt="csv"):
        """
        对于每个板块,获得这个板块下所有二手房的信息
        并且将这些信息写入文件保存
        :param city_pinyin_name: 城市
        :param area_pinyin_name: 板块
        :param fmt: 保存文件格式
        :return: None
        """
        district_pinyin_name = area_district_pinyin_name_dict.get(area_pinyin_name, "")
        csv_file = self.today_path + "/{0}_{1}.csv".format(district_pinyin_name, area_pinyin_name)
        ershous = self.get_area_ershou_info(self.date_string, city_pinyin_name, area_pinyin_name)
        if len(ershous) == 0:
            print("{0}-{1} 没有在售住宅".format(district_pinyin_name, area_pinyin_name))
            return

        with open(csv_file, "w") as f:
            # 开始获得需要的板块数据
            # 锁定，多线程读写
            if self.mutex.acquire(1):
                self.total_num += len(ershous)
                self.ershou_analyzer.add_area_houses_info_to_dict(district_pinyin_name,
                                                                  area_pinyin_name,
                                                                  ershous)
                # 释放
                self.mutex.release()
            if fmt == "csv":
                f.write(ErShou.excel_title) # write first row(title) of csv file
                for ershou in ershous:
                    # print(date_string + "," + xiaoqu.text())
                    f.write(ershou.text())
        print("Finish crawl area: " + area_pinyin_name + ", save data to : " + csv_file)

    @staticmethod
    def get_area_ershou_info(date_string, city_pinyin_name, area_pinyin_name):
        """
        通过爬取页面获得城市指定版块的二手房信息
        :param city_pinyin_name: 城市
        :param area_pinyin_name: 版块
        :return: 二手房数据列表
        """
        total_page = 1
        district_pinyin_name = area_district_pinyin_name_dict.get(area_pinyin_name, "")
        # 中文区县
        district_cn_name = get_district_cn_name(district_pinyin_name)
        # 中文版块
        area_cn_name = area_pinyin_cn_name_dict.get(area_pinyin_name, "")

        ershou_list = list()
        page = 'http://{0}.{1}.com/ershoufang/{2}/'.format(city_pinyin_name, SPIDER_NAME, area_pinyin_name)
        print(page)  # 打印版块页面地址
        headers = create_headers()
        response = requests.get(page, timeout=50, headers=headers)
        html = response.content
        soup = BeautifulSoup(html, "lxml")

        # 获得总的页数，通过查找总页码的元素信息
        try:
            page_box_class = 'page-box house-lst-page-box'
            page_box = soup.find_all('div', class_=page_box_class)
            matches = re.search('.*"totalPage":(\d+),.*', str(page_box))
            total_page = int(matches.group(1))
            print("{0}.total_page: {1}".format(area_pinyin_name, total_page))
        except Exception as e:
            print("\tWarning: only find one page for {0}".format(area_pinyin_name))
            print(e)


        # 从第一页开始,一直遍历到最后一页
        for num in range(1, total_page + 1):
            page = 'http://{0}.{1}.com/ershoufang/{2}/pg{3}'.format(city_pinyin_name, SPIDER_NAME, area_pinyin_name, num)
            print(page)  # 打印每一页的地址
            headers = create_headers()
            BaseSpider.random_delay()
            response = requests.get(page, timeout=10, headers=headers)
            html = response.content
            soup = BeautifulSoup(html, "lxml")
            #print("debug soup: ", soup)

            li_class = 'clear LOGVIEWDATA LOGCLICKDATA'
            totalprice_class = 'totalPrice totalPrice2'
            unitprice_class = 'unitPrice'
            position_class = 'positionInfo'
            title_class = 'title'
            house_class = 'houseInfo'
            img_class = 'lj-lazy'
            # 获得有小区信息的panel
            house_elements = soup.find_all('li', class_=li_class)
            #print("debug, house_elements: ", house_elements)
            for house_elem in house_elements:
                title = house_elem.find('div', class_=title_class)
                position = house_elem.find('div', class_=position_class)
                total_price = house_elem.find('div', class_=totalprice_class)
                unit_price = house_elem.find('div', class_=unitprice_class)
                desc = house_elem.find('div', class_=house_class)
                pic = house_elem.find('img', class_=img_class)

                # 继续清理数据
                #print(title.text.strip)
                #print(position.text)
                #print(total_price.text)
                #print(unit_price.text)
                #print(desc.text)
                #print(pic.get('data-original'))
                title_text = title.text.replace("\n", "").replace(",", "").strip()
                position_text = position.text.replace("\n", "").replace(",", "").strip()
                total_price_text = total_price.text.replace(",", "").replace("万", "").strip()
                unit_price_text = unit_price.text.replace(",", "").replace("元/平","").strip()
                desc_text = desc.text.replace("\n", "").replace(",", "").strip()
                pic_url = pic.get('data-original').replace(",", "").strip()
                if len(pic_url) == 0:
                    pic_url = "no pic url"

                # 作为对象保存
                ershou = ErShou(date_string, district_cn_name, area_cn_name, title_text,
                                unit_price_text, total_price_text, position_text, desc_text, pic_url)
                ershou_list.append(ershou)
        return ershou_list

    def start(self):
        city = get_city()
        self.city_pinyin_name = city
        self.today_path = create_date_path("{0}/ershou".format(SPIDER_NAME), city, self.date_string)
        self.summary_path = create_summary_path("{0}/ershou".format(SPIDER_NAME), city)
        self.ershou_analyzer.set_base_info(self.city_pinyin_name, self.summary_path)

        t1 = time.time()  # 开始计时

        # 获得城市有多少区列表, district: 区县
        districts_pinyin_names = get_districts(city)
        print('City: {0}'.format(city))
        print('districts_pinyin_names: {0}'.format(districts_pinyin_names))

        # 获得每个区的板块, area: 板块
        area_pinyin_names_list = list()
        for district_pinyin_name in districts_pinyin_names:
            area_pinyin_names_of_district = get_areas(city, district_pinyin_name)
            print('{0}: Area list:  {1}'.format(district_pinyin_name, area_pinyin_names_of_district))
            # 用list的extend方法,L1.extend(L2)，该方法将参数L2的全部元素添加到L1的尾部
            area_pinyin_names_list.extend(area_pinyin_names_of_district)
            # 使用一个字典来存储区县和板块的对应关系, 例如{'beicai': 'pudongxinqu', }
            for area_pinyin_name in area_pinyin_names_of_district:
                area_district_pinyin_name_dict[area_pinyin_name] = district_pinyin_name
        print("Area:", area_pinyin_names_list)
        print("District and areas:", area_district_pinyin_name_dict)

        # 准备线程池用到的参数
        nones = [None for i in range(len(area_pinyin_names_list))]
        city_list = [city for i in range(len(area_pinyin_names_list))]
        args = zip(zip(city_list, area_pinyin_names_list), nones)

        # 针对每个板块写一个文件,启动一个线程来操作
        pool_size = thread_pool_size
        pool = threadpool.ThreadPool(pool_size)
        my_requests = threadpool.makeRequests(self.collect_area_ershou_data, args)
        [pool.putRequest(req) for req in my_requests]
        pool.wait()
        pool.dismissWorkers(pool_size, do_join=True)  # 完成后退出

        # 计时结束，统计结果
        t2 = time.time()
        print("Total crawl {0} areas.".format(len(area_pinyin_names_list)))
        print("Total cost {0} second to crawl {1} data items.".format(t2 - t1, self.total_num))

        self.ershou_analyzer.data_analyzer()


if __name__ == '__main__':
    pass
