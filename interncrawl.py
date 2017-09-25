# -*- coding: utf-8 -*-
import scrapy
from selenium import webdriver
from interninfo.items import InterninfoItem
from scrapy.xlib.pydispatch import dispatcher
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from scrapy import signals
from lxml import etree

class InterncrawlSpider(scrapy.Spider):
    name = "interncrawl"
    allowed_domains = ["www.newsmth.net"]
    #定义起始页
    url = 'http://www.newsmth.net/nForum/board/Intern?p='
    page = 1
    start_urls = [url+str(page)]
    
    def __init__(self):
        scrapy.spiders.Spider.__init__(self)
        #定义phantomjs浏览器
        self.driver = webdriver.PhantomJS()
        self.driver.set_page_load_timeout(20)
        self.driver.set_window_size(2000,2000)
        #设置分离器让爬虫退出的时候关闭浏览器
        dispatcher.connect(self.spider_closed,signals.spider_closed)

    def spider_closed(self, spider):
        self.driver.quit()

    def parse(self, response):
        #让浏览器去访问scrapy已经取得的页面
        #print response.url
        self.driver.get(response.url)
        #首先设置显式等待直到页面被完全加载，该条件会一直循环
        try:
            element = WebDriverWait(self.driver,30).until(EC.presence_of_all_elements_located((By.TAG_NAME,'table')))
            print 'element:\n', element
        except Exception, e:
            print Exception, ":", e
            print "wait failed"
        #加载完毕后提取页面所有信息    
        page_source = self.driver.page_source
        html = etree.HTML(page_source)
        for each in html.xpath('//td[@class="title_9 bg-odd"] | //td[@class="title_9"]'):
            item = InterninfoItem()
            try:
                #前几条为广告，url的格式与正式帖子不同，这里只单独提取出url，不获取具体的内容
                if each.xpath('./a/@href')[0].startswith('http'):
                    url = each.xpath('./a/@href')[0]
                else:
                    url = 'http://www.newsmth.net' + each.xpath('./a/@href')[0]
                    print url
            except:
                url = ''
            item['url'] = url
            try:
                title = each.xpath('.//a/text()')[0]
                print title
            except:
                title = ''
            item['title'] = title
            #帖子的内容需要根据url进一步访问，故需要另外写一个方法来单独获取链接内容并将url作为参数传入
            content = self.parse_content(url)
            item['content'] = content
            yield item
        #一页提取完以后再次发送请求，注意写上回调函数
        self.page += 1
        if self.page <=4193:
            yield scrapy.Request(self.url+str(self.page),callback = self.parse)
    
    def parse_content(self,url):
        self.driver.get(url)
        #等待加载ajax页面
        try:
            element = WebDriverWait(self.driver,30).until(EC.presence_of_all_elements_located((By.TAG_NAME,'table')))
            print 'element:\n', element
        except Exception, e:
            print Exception, ":", e
            print "wait failed"
        
        page_source = self.driver.page_source
        html = etree.HTML(page_source)
        content = ''
        #因为帖子内容含有br标签，要循环多次提取
        try:
            for p in html.xpath('//div[@class="b-content corner"]/div[1]//p/text()'):
                content += p
        except:
            pass
        return content


        
        
