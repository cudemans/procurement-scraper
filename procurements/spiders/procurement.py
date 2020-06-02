# -*- coding: utf-8 -*-
import scrapy
from scrapy.selector import Selector
from scrapy.http.request import Request
from selenium import webdriver


class ProcurementSpider(scrapy.Spider):
    name = 'procurement'
    # change start url here - this will change for both scrapy and selenium
    url = 'http://search.ccgp.gov.cn/bxsearch?searchtype=1&page_index=1&bidSort=0&buyerName=&projectId=&pinMu=&bidType=7&dbselect=bidx&kw=%E5%85%AC%E5%85%B1%E5%AE%89%E5%85%A8&start_time=2018%3A12%3A03&end_time=2019%3A06%3A02&timeType=6&displayZone=&zoneId=&pppStatus=0&agentName='
    allowed_domains = ['www.ccgp.gov.cn']
    start_urls = [url]

    def __init__(self):

        file_path = '/Users/charlene/Documents/Chris/scraper-driver/chromedriver'
        self.driver = webdriver.Chrome(file_path)

        self.driver.get(self.url)


    def parse(self, response):
        responses = []
        # change number of pages to scrape here
        number_of_pages = 8
        for page in range(number_of_pages):
            responses.append(self.driver.page_source)

            self.driver.execute_script("document.getElementsByClassName('next')[1].click()")
            self.driver.implicitly_wait(15)

        for response in responses:
            resp = Selector(text=response)

            for item in resp.xpath("//ul[@class='vT-srch-result-list-bid']/li"):
                url = item.xpath(".//a/@href").get()


                yield Request(url=url, callback=self.parse_url)


    def parse_url(self, response):
        title = response.xpath("//h2/text()").get()
        project = response.xpath("//td[contains(text(), '采购项目名称')]/following::node()[1]/text()").get()
        procurement_unit = response.xpath("//td[contains(text(), '采购单位')]/following::node()[1]/text()").get()
        region = response.xpath("//td[contains(text(), '行政区域')]/following::node()[1]/text()").get()
        amount = response.xpath("//td[contains(text(), '（人民币）')]/text()").get()
        announce_date = response.xpath("//td[contains(text(), '年')][1]/text()").get()
        link = response.xpath("//a[@class='bizDownload']/@id").get()


        yield {
            'title': title,
            'project': project,
            'procurement unit': procurement_unit,
            'area': region,
            'amount': amount,
            'date': announce_date,
            'documentation': "www.ccgp.gov.cn/oss/download?uuid={}".format(link)
        }
