import scrapy
import re

class DanSpider(scrapy.Spider):
    name = "DanSpider"
    url = "https://www.hbggzyfwpt.cn/jyxx/jsgcZbgg"

    form = {
        "currentPage": "1",
        "area": "000",
        "currentArea": "001",
        "industriesTypeCode": "0",
        "scrollValue": "0",
        "bulletinName": "",
        "publishTimeType": "1",
        "publishTimeStart": "",
                "publishTimeEnd": ""
    }

    def start_requests(self):
        yield scrapy.FormRequest(url=self.url, formdata=self.form, callback=self.parseCount)
        return super().start_requests()
    
    def parseCount(self, response):
        data=response.css('div.mmggxlh a::text').getall()
        print("---------------------")
        print(int(data[-2]))
        count = int(data[-2])
        
        for i in range(2, count+1):
            self.form['currentPage']=str(i)
            print(self.form)
            yield scrapy.FormRequest(url=self.url, formdata=self.form, callback=self.parseItem)
      
            
    def parseItem(self, response, **kwargs):
        pass       
