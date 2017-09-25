# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import json


#将结果写入本地json文件中
class InterninfoPipeline(object):
    def __init__(self):
        self.writer = open('anfo.json','w')
    def process_item(self, item, spider):
        text = json.dumps(dict(item),ensure_ascii=False) +'\n'
        self.writer.write(text.encode('utf-8'))
        return item
    def close_spider(self,spider):
        self.writer.close()
