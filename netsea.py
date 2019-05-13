import requests
from lxml import html
from lxml import etree
from bs4 import BeautifulSoup
import csv



class NetseaSpider:

    def __init__(self):
        self.id = 1


    def get_links(self, url='https://www.netsea.jp/newitem'):
        URL = requests.get(url)
        tree = html.fromstring(URL.content)
        self.links_Xpath = tree.xpath('//div[@class="showcaseBox"]//h3/a/@href')
        self.parse_pages(self.links_Xpath)
        try:
            next_page_url = tree.xpath('//li[@class="next"]/a/@href')[0]
            if next_page_url:
                print(next_page_url)
                self.get_links(next_page_url)
        except IndexError:
            pass


    def parse_pages(self, links):
        for url in links:
            r = requests.get(url)
            self.get_info(r)


    def get_info(self, page):
        tree = html.fromstring(page.content)
        title = tree.xpath('//div[@id="contentsArea"]/h1/text()')[0]
        try:
            category = tree.xpath('//section[@id="itemSummarySec"]//h4[contains(@class, "hdType04")]/text()')[0]
        except IndexError:
            category = ''
        size = tree.xpath('//section[@id="itemDetailSec"]//table[@class="tableType02"]/tbody/tr/td')[0]
        size = etree.tostring(size, pretty_print=True)
        size = [i.text.replace("\t", " ").strip() for i in BeautifulSoup(size, 'lxml')]
        size = ''.join(size)
        standart = tree.xpath('//section[@id="itemDetailSec"]//table[@class="tableType02"]/tbody/tr/td')[1]
        standart = etree.tostring(standart, pretty_print=True)
        standart = [i.text.strip() for i in BeautifulSoup(standart, 'lxml')]
        standart = ''.join(standart)
        delivery_terms = tree.xpath('//section[@id="itemDetailSec"]//table[@class="tableType02"]/tbody/tr/td')[3]
        delivery_terms = etree.tostring(delivery_terms, pretty_print=True)
        delivery_terms = [i.text.strip() for i in BeautifulSoup(delivery_terms, 'lxml')]
        delivery_terms = ''.join(delivery_terms)
        purchas_returns = tree.xpath('//section[@id="itemDetailSec"]//table[@class="tableType02"]/tbody/tr/td')[4]
        purchas_returns = etree.tostring(purchas_returns, pretty_print=True)
        purchas_returns = [i.text.strip() for i in BeautifulSoup(purchas_returns, 'lxml')]
        purchas_returns = ''.join(purchas_returns)
        order = tree.xpath('//section[@id="itemDetailSec"]//table[@class="tableType02"]/tbody/tr/td')[5]
        order = etree.tostring(order, pretty_print=True)
        order = [i.text.strip() for i in BeautifulSoup(order, 'lxml')]
        order = ''.join(order)
        code = tree.xpath('//section[@id="itemDetailSec"]//table[@class="tableType02"]/tbody/tr/td')[6]
        code = etree.tostring(code, pretty_print=True)
        code = [i.text.strip() for i in BeautifulSoup(code, 'lxml')]
        code = ''.join(code)
        url = page.url


        row = [self.id, title, category, size, standart, delivery_terms, purchas_returns, order, code, url]

        with open('netsea.csv', 'a', encoding='utf-8-sig') as f:
            wr = csv.writer(f, dialect='excel')
            wr.writerow(row)
        self.id = self.id + 1


def create_new_csv():
    table_headers = ['id', '商品タイトル', '商品紹介', 'サイズ・容量', '規格', '出荷条件', '良品返品', '注文について',
                 'JANコード', 'url']
    with open('netsea.csv', 'w', encoding='utf-8-sig') as f:
        wr = csv.writer(f, dialect='excel')
        wr.writerow(table_headers)


if __name__ == '__main__':
    create_new_csv()
    spider = NetseaSpider()
    spider.get_links()
