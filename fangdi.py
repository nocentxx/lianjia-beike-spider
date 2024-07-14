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

    def get_sh_yesterday_sell(self):
        #POST /oldhouse/getSHYesterdaySell.action?MmEwMD=4Btes6wob5ZKKkDwBbM7k01vFxy5wGaxJQnMJOrohYRZIR1HDgxldVE0Fl5NfjmgB6u.tYurEOc.HAsf1NKaY6NsUmEV9NSLCzzHnmO6gMrOBcEHrByq3ab4As0RvYQCvkq8ffyWuvuz3ieorbPknIyw6f4AW4cYzPPhF1AmdQcnupQy7G7IWQTj.hLs0EKgYMFWhf.c03_tFU0ZKorK_IHS_NUgEzDYwhZ7FIifcL6SIkWIzB9yQRjuWCbD6GIG2mIR.lTKjx8gFcQn7FEHQ8w6QJxMtPq.b1csyySHKyLq4Lg.l9NCXoQjGicCQtWhJddgGt9RYQ.Vwoh2srwwvH9RRjjwE57btzIYp7OQg567aHyuj7eZ3nLyHutSPVITa4KR HTTP/1.1
        headers = dict()
        #headers['Accept'] = 'application/json, text/javascript, */*; q=0.01'
        #headers['Accept-Encoding'] = 'gzip, deflate'
        #headers['Accept-Language'] = 'zh-CN,zh;q=0.9,en;q=0.8'
        #headers['Connection'] = 'keep-alive'
        #headers['Content-Length'] = '0'
        headers['Content-Type'] = 'application/x-www-form-urlencoded;charset=utf-8'
        #headers['Cookie'] = 'www.fangdi.com_http_ic=www.fangdi.com.cn_80_RS; www.fangdi.com.cn=www.fangdi.com.cn_rs4; FSSBBIl1UgzbN7N80S=w6iZD4fRq4c4f8Tqc1fP1r9SkgSFDjwc6gi2Fbr3q8EQJe4B_MKtgYHvMDc.KtKO; www.fangdi.com_http_ic=www.fangdi.com.cn_80_RS; JSESSIONID1=RXyTVMSCkIOvN3AkVLFme7z_6B4jDSecQ1iFQE3Hg8nrKKy4XwOv!15736515; FSSBBIl1UgzbN7N80T=41TP9tP3pkkxf5yc3M9u0xzgz0DfjwHK_fJl_853ZLbOL9zASmCMEN6.zyrCKU_v3tW0eLW8d8e0gz752VNBPtKWGZKWaSXzm71aTpuS8s3XNx7B6XTR3vPaEwwFYmKQRXrNmtBINnL58qDwqaGhTBFmM9xqLMFFqeKgUenSBqoNPZn58ZxphYnnp6MwJdGoJq2Vy17gDkGeLfMXQWnJraws2YGx59lyjvk39oFMIo0juHLhE3WBzmwrWK5Yi_lUHv3bPqRfrnH1xZWKKhW8xbeYgsA2dRQxghfIFdF9.W1Kd8Z5pMIRk18MYJQDI2.YW4kQ'
        #headers['DNT'] = '1'
        #headers['Host'] = 'www.fangdi.com.cn'
        #headers['Origin'] = 'http://www.fangdi.com.cn'
        headers['Referer'] = 'http://www.fangdi.com.cn/old_house/old_house.html'
        headers['User-Agent'] = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        headers['X-Requested-With'] = 'XMLHttpRequest'

        params = dict()
        params['MmEwMD'] = '4Btes6wob5ZKKkDwBbM7k01vFxy5wGaxJQnMJOrohYRZIR1HDgxldVE0Fl5NfjmgB6u.tYurEOc.HAsf1NKaY6NsUmEV9NSLCzzHnmO6gMrOBcEHrByq3ab4As0RvYQCvkq8ffyWuvuz3ieorbPknIyw6f4AW4cYzPPhF1AmdQcnupQy7G7IWQTj.hLs0EKgYMFWhf.c03_tFU0ZKorK_IHS_NUgEzDYwhZ7FIifcL6SIkWIzB9yQRjuWCbD6GIG2mIR.lTKjx8gFcQn7FEHQ8w6QJxMtPq.b1csyySHKyLq4Lg.l9NCXoQjGicCQtWhJddgGt9RYQ.Vwoh2srwwvH9RRjjwE57btzIYp7OQg567aHyuj7eZ3nLyHutSPVITa4KR'
        #url = 'http://www.fangdi.com.cn/oldhouse/getSHYesterdaySell.action?MmEwMD=4Btes6wob5ZKKkDwBbM7k01vFxy5wGaxJQnMJOrohYRZIR1HDgxldVE0Fl5NfjmgB6u.tYurEOc.HAsf1NKaY6NsUmEV9NSLCzzHnmO6gMrOBcEHrByq3ab4As0RvYQCvkq8ffyWuvuz3ieorbPknIyw6f4AW4cYzPPhF1AmdQcnupQy7G7IWQTj.hLs0EKgYMFWhf.c03_tFU0ZKorK_IHS_NUgEzDYwhZ7FIifcL6SIkWIzB9yQRjuWCbD6GIG2mIR.lTKjx8gFcQn7FEHQ8w6QJxMtPq.b1csyySHKyLq4Lg.l9NCXoQjGicCQtWhJddgGt9RYQ.Vwoh2srwwvH9RRjjwE57btzIYp7OQg567aHyuj7eZ3nLyHutSPVITa4KR'
        url = 'http://www.fangdi.com.cn/oldhouse/getSHYesterdaySell.action?'

        response = requests.post(url=url, headers=headers)
        print(response.url)
        print(response.text)
        print(response.status_code)

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
    fangdi.get_sh_yesterday_sell()
    #fangdi.get_newhouse_info("123")
