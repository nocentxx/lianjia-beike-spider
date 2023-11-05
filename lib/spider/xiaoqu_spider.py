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
    def collect_area_xiaoqu_data(self, city_py, area_py, fmt="csv"):
        """
        对于每个板块,获得这个板块下所有小区的信息
        并且将这些信息写入文件保存
        :param city_py: 城市
        :param area_py: 板块
        :param fmt: 保存文件格式
        :return: None
        """
        district_py = area_district_pinyin_name_dict.get(area_py, "")

        district_cn = district_pinyin_cn_name_dict[district_py]
        area_cn = area_pinyin_cn_name_dict[area_py]

        area_path = create_area_path(self.today_path, district_cn, area_cn)

        area_xiaoqu_csv_file = area_path + "/{0}_{1}.csv".format(district_cn, area_cn)
        xqs = self.get_xiaoqu_info(city_py, area_py, area_path)
        with open(area_xiaoqu_csv_file, "w") as f:
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
                        #print(self.date_string + "," + xiaoqu.text())

        print("Finish crawl area: " + area_py + ", save data to : " + area_xiaoqu_csv_file)
        logger.info("Finish crawl area: " + area_py + ", save data to : " + area_xiaoqu_csv_file)


    @staticmethod
    def get_xiaoqu_detail(url, subway_info, store_path):
        headers_tmp = create_headers()
        BaseSpider.random_delay()
        response = requests.get(url, timeout=20, headers=headers_tmp)
        html = response.content
        soup = BeautifulSoup(html, "lxml")

        detailTitle = soup.find('h1', class_='detailTitle').text.strip()

        # 小区详细信息
        detail_items = soup.find_all('div', class_='xiaoquDescribe fr')
        for detail_item in detail_items:
            aver_price = detail_item.find('span', class_='noPrice').text
            info_item_list = detail_item.find_all('div', class_='xiaoquInfoItem')

            for info_item in info_item_list:
                label = info_item.find('span', class_='xiaoquInfoLabel').text
                content = info_item.find('span', class_='xiaoquInfoContent').text
                if label == '建筑类型':
                    building_type = content
                elif label == '房屋总数':
                    house_total = content
                elif label == '楼栋总数':
                    building_total = content
                elif label == '绿化率':
                    greening_ratio = content
                elif label == '容积率':
                    plot_ratio = content
                elif label == '交易权属':
                    trade_type = content
                elif label == '建成年代':
                    built_year = content
                elif label == '供暖类型':
                    heating_type = content
                elif label == '用水类型':
                    water_type = content
                elif label == '用电类型':
                    elec_type = content
                elif label == '物业费':
                    property_fee = content
                elif label == '附近门店':
                    intermediary = content
                elif label == '物业公司':
                    property_company = content
                elif label == '开发商':
                    real_estate = content
                else:
                    print('error! unknown label: ', label)

        #print("detail: ", trade_type, built_year, aver_price, building_type, \
        #        house_total, building_total, greening_ratio, plot_ratio, \
        #        water_type, elec_type, heating_type, subway_info, \
        #        property_fee, property_company, real_estate, intermediary)

        xiaoqu_csv_file = store_path + "/" + detailTitle + ".csv"
        if not os.path.isfile(xiaoqu_csv_file):
            with open(xiaoqu_csv_file, "w") as f:
                f.write(DealFrame.deal_frame_title) # write first row(title) of csv file

        # 小区成交记录
        cj_records = soup.find_all('ol', class_='frameDealListItem')#.find_all('li')
        for cj_record in cj_records:
            cj_item_list = cj_record.find_all('li')
            with open(xiaoqu_csv_file, "a") as f:
                for cj_item in cj_item_list:
                    dealDesc = cj_item.find('div', class_='frameDealDesc').text
                    dealArea = cj_item.find('div', class_='frameDealArea').text
                    dealDate = cj_item.find('div', class_='frameDealDate').text
                    dealPrice = cj_item.find('div', class_='frameDealPrice').text
                    dealUnitPrice = cj_item.find('div', class_='frameDealUnitPrice').text

                    deal_frame = DealFrame(dealDate, dealArea, dealPrice, dealUnitPrice, dealDesc, detailTitle, \
                        trade_type, built_year, aver_price, building_type, \
                        house_total, building_total, greening_ratio, plot_ratio, \
                        water_type, elec_type, heating_type, subway_info, \
                        property_fee, property_company, real_estate, intermediary)

                    f.write(deal_frame.text())
                    #print(deal_frame.text())

    @staticmethod
    def get_xiaoqu_info(city, area, store_path):
        total_page = 1
        district = area_district_pinyin_name_dict.get(area, "")
        district_cn_name = get_district_cn_name(district)
        area_cn_name = area_pinyin_cn_name_dict.get(area, "")
        xiaoqu_list = list()
        page = 'http://{0}.{1}.com/xiaoqu/{2}/'.format(city, SPIDER_NAME, area)

        headers = create_headers()
        response = requests.get(page, timeout=20, headers=headers)
        html = response.content
        soup = BeautifulSoup(html, "lxml")

        # 获得总的页数
        try:
            result_desc = soup.find_all('h2', class_='total fl')
            #print("rest desc:", result_desc)
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
            #print('total_page: ', total_page)
        except Exception as e:
            print("\tWarning: only find one page for {0}".format(area))
            print('Exception: ', e)

        # 从第一页开始,一直遍历到最后一页
        for i in range(1, total_page + 1):
            headers_tmp = create_headers()
            page = 'http://{0}.{1}.com/xiaoqu/{2}/pg{3}'.format(city, SPIDER_NAME, area, i)
            print("xiaoqu url: ", page)
            BaseSpider.random_delay()
            response = requests.get(page, timeout=20, headers=headers_tmp)
            html = response.content
            soup = BeautifulSoup(html, "lxml")

            # 获得有小区信息的panel
            house_elems = soup.find_all('li', class_="clear xiaoquListItem")
            for house_elem in house_elems:
                #<a class="img" href="https://sh.lianjia.com/xiaoqu/5011000002150/" target="_blank">
                #<img alt="东海三村" class="lj-lazy" data-original="https://image1.ljcdn.com/hdic-resblock/e2eb1a5e-28eb-4d87-8016-12beedd0dfca.jpg.232x174.jpg" src="https://s1.ljcdn.com/feroot/pc/asset/img/blank.gif?_v=20231101121207"/>
                #</a>
                xq_url = house_elem.find('a', class_='img').get('href')

                xq_name = house_elem.find('div', class_='title').text.replace("\n", "").strip()
                position = house_elem.find('div', class_='positionInfo').text.replace("\n", "").strip().split(sep='/')
                built_year = re.sub('年.*', '', position[1].strip())

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

                XiaoQuBaseSpider.get_xiaoqu_detail(xq_url, subway_info, store_path) # 小区详细信息

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

        # 获得每个区的板块, area: 板块
        areas_py_names_list = list()
        for district_pinyin_name in districts_pinyin_names:
            areas_py_of_district = get_areas(city, district_pinyin_name)
            # 用list的extend方法,L1.extend(L2)，该方法将参数L2的全部元素添加到L1的尾部
            areas_py_names_list.extend(areas_py_of_district)
            # 使用一个字典来存储区县和板块的对应关系, 例如{'beicai': 'pudongxinqu', }
            for area in areas_py_of_district:
                area_district_pinyin_name_dict[area] = district_pinyin_name

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
