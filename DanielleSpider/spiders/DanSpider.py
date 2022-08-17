import scrapy
from scrapy.loader import ItemLoader
from DanielleSpider.items import DaniellespiderItem

class DanSpider(scrapy.Spider):
    name = "DanSpider"
    urls = [{"url": "https://www.hbggzyfwpt.cn/jyxx/jsgcZbgg", "sheetName": "招标信息汇总"},
            # {"url": "https://www.hbggzyfwpt.cn/jyxx/jsgcZbjggs", "sheetName": "中标信息汇总"}
            ]

    form = {
        "currentPage": "1",
        "area": "000",
        "currentArea": "001",
        "industriesTypeCode": "2",
        "scrollValue": "0",
        "bulletinName": "",
        "publishTimeType": "2",
        "publishTimeStart": "",
        "publishTimeEnd": ""
    }
    
    industriesTypeCodes = ["2", "4", "5"]

    def start_requests(self):
        for url in self.urls:
            for industriesTypeCode in self.industriesTypeCodes:
                self.form["industriesTypeCode"] = industriesTypeCode
                yield scrapy.FormRequest(url=url['url'], formdata=self.form, callback=self.parseCount, meta=url)
        # return super().start_requests()
    
    def parseCount(self, response):
        mm = response.meta
        data=response.css('div.mmggxlh a::text').getall()
        print("---------------------")
        # print(mm)
        # print('page', int(data[-2]))
        count = int(data[-2])
        
        self.parseItem(response=response)
        for i in range(2, count+1):
            self.form['currentPage']=str(i)
            # print(self.form)
            # yield scrapy.FormRequest(url=self.url, formdata=self.form, callback=self.parseItem)
      
            
    def parseItem(self, response):
        print("------**********-----start")
        # data = response.css('div.newListwenzi table').getall()
        data = response.xpath('//div/table').xpath('//a[contains(@href, "Detail")]').getall()
        print('count', len(data))
        print("------**********-----end")
