# scrapy-ajax-
此项目基于scrapy+selenium+phantomjs来获取动态加载的页面内容

示例网站：http://www.newsmth.net/nForum/board/Intern

采集字段在items.py文件中，采集程序为interncrawl.py，示例结果写在anfo.json文件中（只爬取了其中的500多条）

因为该网站的反爬措施比较简单，添加一个user-agent就够了，也没加入其它手段。
