import requests

from bs4 import BeautifulSoup
from lib.request.headers import create_headers
from lib.utility.date import *
from lib.utility.log import *
from lib.utility.path import *

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

class ShangHaiFangdi(object):
    def __init__(self):
        # 准备日期信息，爬到的数据存放到日期相关文件夹下
        self.date_string = get_date_string()
        self.today_path = create_date_path("fangdi", "shanghai", self.date_string)
        self.oldhouse_page = 'http://www.fangdi.com.cn/old_house/old_house.html'
        self.newhouse_page = 'http://www.fangdi.com.cn/index.html'

        logger.info("oldhouse page: " + self.oldhouse_page)
        logger.info("newhouse page: " + self.newhouse_page)

    def run_javascript(self, page):
        # 创建Chrome浏览器实例
        chrome_service = Service(executable_path='/opt/google/chrome/chromedriver')
        chrome_options = Options()
        chrome_options.add_argument('--headless')  # 无头模式
        #chrome_options.add_argument('--proxy-server=http://%s:%s@%s:%s' % (proxyUser, proxyPass, proxyHost, proxyPort))
        driver = webdriver.Chrome(options=chrome_options, service=chrome_service)

        # 打开网页
        print('url: ', page)
        driver.get(page)

        # 等待页面加载完成
        driver.implicitly_wait(15)

        # 获取页面内容
        page_content = driver.page_source
        print('url page content: ', page_content)

        # 关闭浏览器实例
        driver.quit()

        return page_content

    def get_newhouse_info(self, filename):
        html = self.run_javascript(self.newhouse_page)
        soup = BeautifulSoup(html, "html.parser")
        print("url request, request success")

        # 获得总的页数
        try:
            result_desc = soup.find_all('div', class_='main_item_right')
            print("rest desc:", result_desc)
            #matches = re.search('.*<span> (\d+) </span>', str(result_desc))
            #result_num = int(matches.group(1))
            #if result_num == 0:
            #    print('warning: no xiaoqu found, ignore in ', area_cn_name)
            #    return xiaoqu_list
        except Exception as e:
            print("Exception: ", e)
            #return xiaoqu_list


    def get_oldhouse_info(self, filename):
        headers = create_headers()
        response = requests.get(self.oldhouse_page, timeout=20, headers=headers)
        html = response.content
        soup = BeautifulSoup(html, "lxml")
        print("url request, get xiaoqu success")

        # 获得总的页数
        try:
            result_desc = soup.find_all('div', class_='sign_top1')
            print("rest desc:", result_desc)
            #matches = re.search('.*<span> (\d+) </span>', str(result_desc))
            #result_num = int(matches.group(1))
            #if result_num == 0:
            #    print('warning: no xiaoqu found, ignore in ', area_cn_name)
            #    return xiaoqu_list
        except Exception as e:
            print("Exception: ", e)
            #return xiaoqu_list

if __name__ == "__main__":
    fangdi = ShangHaiFangdi()
    fangdi.get_newhouse_info("123")
