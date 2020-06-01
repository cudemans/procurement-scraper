# -*- coding: utf-8 -*-
import scrapy
from scrapy.selector import Selector
from scrapy.http.request import Request
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait


class ProcurementSpider(scrapy.Spider):
    name = 'procurement'
    allowed_domains = ['www.ccgp.gov.cn']
    start_urls = ['http://search.ccgp.gov.cn/bxsearch?searchtype=2&page_index=1&bidSort=&buyerName=&projectId=&pinMu=&bidType=&dbselect=bidx&kw=%E5%AE%89%E9%98%B2&start_time=2019%3A12%3A02&end_time=2020%3A06%3A01&timeType=5&displayZone=&zoneId=&pppStatus=0&agentName=']

    def __init__(self):

        file_path = '/Users/charlene/Documents/Chris/scraper-driver/chromedriver'
        self.driver = webdriver.Chrome(file_path)

        self.driver.get("http://search.ccgp.gov.cn/bxsearch?searchtype=2&page_index=1&bidSort=&buyerName=&projectId=&pinMu=&bidType=&dbselect=bidx&kw=%E5%AE%89%E9%98%B2&start_time=2019%3A12%3A02&end_time=2020%3A06%3A01&timeType=5&displayZone=&zoneId=&pppStatus=0&agentName=")


    def parse(self, response):
        responses = []
        number_of_pages = 196
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
        region = response.xpath("//td[contains(text(), '行政区域')]/following::node()[1]/text()").get()
        amount = response.xpath("//td[contains(text(), '（人民币）')]/text()").get()
        announce_date = response.xpath("//td[contains(text(), '年')][1]/text()").get()

        yield {
            'title': title,
            'project': project,
            'area': region,
            'amount': amount,
            'date': announce_date
        }
