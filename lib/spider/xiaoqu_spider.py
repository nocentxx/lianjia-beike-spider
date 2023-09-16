#!/usr/bin/env python
# coding=utf-8
# author: zengyuetian
# 此代码仅供学习与交流，请勿用于商业用途。
# 爬取小区数据的爬虫派生类

import re
import threadpool
from bs4 import BeautifulSoup
from lib.item.xiaoqu import *
from lib.zone.city import get_city
from lib.spider.base_spider import *
from lib.utility.date import *
from lib.utility.path import *
from lib.zone.area import *
from lib.utility.log import *
import lib.utility.version


class XiaoQuBaseSpider(BaseSpider):
    def collect_area_xiaoqu_data(self, city_name, area_name, fmt="csv"):
        """
        对于每个板块,获得这个板块下所有小区的信息
        并且将这些信息写入文件保存
        :param city_name: 城市
        :param area_name: 板块
        :param fmt: 保存文件格式
        :return: None
        """
        district_name = area_district_pinyin_name_dict.get(area_name, "")
        csv_file = self.today_path + "/{0}_{1}.csv".format(district_name, area_name)
        xqs = self.get_xiaoqu_info(city_name, area_name)
        with open(csv_file, "w") as f:
            # 开始获得需要的板块数据
            # 锁定
            if self.mutex.acquire(1):
                self.total_num += len(xqs)
                # 释放
                self.mutex.release()
            if fmt == "csv":
                if len(xqs) > 0:
                    f.write(XiaoQu.xiaoqu_title)
                    for xiaoqu in xqs:
                        f.write(self.date_string + "," + xiaoqu.text())
        print("Finish crawl area: " + area_name + ", save data to : " + csv_file)
        logger.info("Finish crawl area: " + area_name + ", save data to : " + csv_file)

    @staticmethod
    def get_xiaoqu_info(city, area):
        total_page = 1
        district = area_district_pinyin_name_dict.get(area, "")
        district_cn_name = get_district_cn_name(district)
        area_cn_name = area_pinyin_cn_name_dict.get(area, "")
        xiaoqu_list = list()
        page = 'http://{0}.{1}.com/xiaoqu/{2}/'.format(city, SPIDER_NAME, area)
        print(page)
        logger.info(page)

        headers = create_headers()
        response = requests.get(page, timeout=10, headers=headers)
        html = response.content
        soup = BeautifulSoup(html, "lxml")
        print("url request, get xiaoqu success")

        # 获得总的页数
        try:
            result_desc = soup.find_all('h2', class_='total fl')
            print("rest desc:", result_desc)
            matches = re.search('.*<span> (\d+) </span>', str(result_desc))
            result_num = int(matches.group(1))
            if result_num == 0:
                print('warning: no xiaoqu found, ignore in ', area_cn_name)
                return xiaoqu_list
        except Exception as e:
            print("Exception: ", e)
            return xiaoqu_list

        try:
            page_box = soup.find_all('div', class_='page-box house-lst-page-box')[0]
            matches = re.search('.*"totalPage":(\d+),.*', str(page_box))
            total_page = int(matches.group(1))
            print('total_page: ', total_page)
        except Exception as e:
            print("\tWarning: only find one page for {0}".format(area))
            print('Exception: ', e)

        # 从第一页开始,一直遍历到最后一页
        for i in range(1, total_page + 1):
            headers = create_headers()
            page = 'http://{0}.{1}.com/xiaoqu/{2}/pg{3}'.format(city, SPIDER_NAME, area, i)
            print(page)  # 打印版块页面地址
            BaseSpider.random_delay()
            response = requests.get(page, timeout=10, headers=headers)
            html = response.content
            soup = BeautifulSoup(html, "lxml")

            # 获得有小区信息的panel
            house_elems = soup.find_all('li', class_="clear xiaoquListItem")
            for house_elem in house_elems:
                xq_name = house_elem.find('div', class_='title').text.replace("\n", "").strip()
                position = house_elem.find('div', class_='positionInfo').text.replace("\n", "").strip().split(sep='/')
                built_year = position[1].strip().replace("年建成", "")

                house_info = house_elem.find('div', class_="houseInfo").text.replace("\n", "").strip().split(sep='|')
                deal_of_90days = house_info[0].strip().replace("90天成交", "").replace("套", "")
                on_rent_count = house_info[1].strip().replace("套正在出租", "")

                price = house_elem.find('div', class_="totalPrice noPrice").text.replace("\n", "").strip()
                on_sale_count = house_elem.find('div', class_="xiaoquListItemSellCount").text.replace("\n", "").replace("套在售二手房", "").strip()
                subway_info = 'n/a'
                try:
                    subway_info = house_elem.find('div', class_="tagList").text.replace("\n", "").strip()
                except Exception as e:
                    print("no subway info.")

                # 作为对象保存
                xiaoqu = XiaoQu(district_cn_name, area_cn_name, xq_name, built_year, price, on_sale_count, deal_of_90days, on_rent_count, subway_info)
                xiaoqu_list.append(xiaoqu)
        return xiaoqu_list

    def start(self):
        city = get_city()
        self.city_pinyin_name = city
        self.today_path = create_date_path("{0}/xiaoqu".format(SPIDER_NAME), city, self.date_string)
        t1 = time.time()  # 开始计时

        # 获得城市有多少区列表, district: 区县
        districts_pinyin_names = get_districts(city)
        print('City: {0}'.format(city))
        print('Districts: {0}'.format(districts_pinyin_names))

        # 获得每个区的板块, area: 板块
        areas_py_names_list = list()
        for district_pinyin_name in districts_pinyin_names:
            areas_py_of_district = get_areas(city, district_pinyin_name)
            print('{0}: Area list:  {1}'.format(district_pinyin_name, areas_py_of_district))
            # 用list的extend方法,L1.extend(L2)，该方法将参数L2的全部元素添加到L1的尾部
            areas_py_names_list.extend(areas_py_of_district)
            # 使用一个字典来存储区县和板块的对应关系, 例如{'beicai': 'pudongxinqu', }
            for area in areas_py_of_district:
                area_district_pinyin_name_dict[area] = district_pinyin_name
        print("Area:", areas_py_names_list)
        print("District and areas:", area_district_pinyin_name_dict)

        # 准备线程池用到的参数
        nones = [None for i in range(len(areas_py_names_list))]
        city_list = [city for i in range(len(areas_py_names_list))]
        args = zip(zip(city_list, areas_py_names_list), nones)
        # areas = areas[0: 1]

        # 针对每个板块写一个文件,启动一个线程来操作
        pool_size = thread_pool_size
        pool = threadpool.ThreadPool(pool_size)
        my_requests = threadpool.makeRequests(self.collect_area_xiaoqu_data, args)
        [pool.putRequest(req) for req in my_requests]
        pool.wait()
        pool.dismissWorkers(pool_size, do_join=True)  # 完成后退出

        # 计时结束，统计结果
        t2 = time.time()
        print("Total crawl {0} areas.".format(len(areas_py_names_list)))
        print("Total cost {0} second to crawl {1} data items.".format(t2 - t1, self.total_num))


if __name__ == "__main__":
    # urls = get_xiaoqu_area_urls()
    # print urls
    # get_xiaoqu_info("sh", "beicai")
    spider = XiaoQuBaseSpider("lianjia")
    spider.start()
