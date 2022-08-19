import scrapy
from scrapy.loader import ItemLoader
from DanielleSpider.items import DaniellespiderItem
import json

class DanSpider(scrapy.Spider):
    name = "DanSpider"
    urls = [{"url": "https://www.hbggzyfwpt.cn/jyxx/jsgcZbgg", "sheetName": "招标信息汇总", "ajax_url": "https://www.hbggzyfwpt.cn/jyxxAjax/jsgcZbggLiDetailT"},
            {"url": "https://www.hbggzyfwpt.cn/jyxx/jsgcZbjggs", "sheetName": "中标信息汇总", "ajax_url": "https://www.hbggzyfwpt.cn/jyxxAjax/jsgcZbjgDetailT"}
            ]

    form = {
        "currentPage": "1",
        "area": "000",
        "currentArea": "001",
        "industriesTypeCode": "2",
        "scrollValue": "0",
        "bulletinName": "",
        "publishTimeType": "1",
        "publishTimeStart": "",
        "publishTimeEnd": ""
    }
    
    industriesTypeCodes = ["2", 
                           "4", 
                           "5"
                           ]

    def start_requests(self):
        for urlObj in self.urls:
            for industriesTypeCode in self.industriesTypeCodes:
                copyForm = {
                    "currentPage": "1",
                    "area": "000",
                    "currentArea": "001",
                    "industriesTypeCode": industriesTypeCode,
                    "scrollValue": "0",
                    "bulletinName": "",
                    "publishTimeType": "0"
                }
                metaInfo = urlObj.copy()
                metaInfo["industriesTypeCode"] = industriesTypeCode
                print(copyForm, urlObj['url'])
                yield scrapy.FormRequest(url=urlObj['url'], formdata=copyForm, callback=self.parseFirstPage, meta=metaInfo)
        # return super().start_requests()
    
    def parseFirstPage(self, response):
        meta = response.meta
        data=response.css('div.mmggxlh a::text').getall()
        print("---------------------")
        # print(mm)
        # print('page', int(data[-2]))
        count = int(data[-2])

        print("---------resp------------",
              response.css('a.pagreActive::text').get())
        # yield self.parseItem(response)
        for i in range(1, count + 1):
            copyForm = {
                "currentPage": str(i),
                "area": "000",
                "currentArea": "001",
                "industriesTypeCode": meta["industriesTypeCode"],
                "scrollValue": "1",
                "bulletinName": "",
                "publishTimeType": "0",
                "publishTimeStart": "",
                "publishTimeEnd": ""
            }
            print(copyForm, meta['url'])
            yield scrapy.FormRequest(url=meta['url'], formdata=copyForm, callback=self.parseItem, meta=meta)
      
    def parseItem(self, response):
        print("------**********-----start")
        meta = response.meta
        # data = response.css('div.newListwenzi table').getall()
        data = response.xpath(
            '//div/table').xpath('//a[contains(@href, "Detail")]/../..')
        pn = response.css('a.pagreActive::text').get()
        print('count', len(data), pn)
        for li in data:
            # print('///////////////////////////////')
            detailUrl = 'https://www.hbggzyfwpt.cn' + li.xpath('td/a/@href').get()            
            source = li.xpath('td/a/font/text()').get()
            # print(detailUrl, source)
            metaInfo = {'detailUrl': detailUrl, 'source': source,
                        "sheetName": meta['sheetName'], "ajax_url": meta['ajax_url']}
            print(metaInfo)
            yield scrapy.Request(url=detailUrl, callback=self.parseDetail, meta=metaInfo)

    def parseDetail(self, response, **kwargs):
        x = response.xpath('//input[@id="bidSectionCode"]/@value').get()
        if x is None:
            return
        form = {"bidSectionCode": x}
        meta = response.meta
        meta["bidSectionCode"] = x
        print("bid", form, meta['ajax_url'])
        yield scrapy.FormRequest(url=meta['ajax_url'], formdata=form, callback=self.parseAjax, meta=meta)
        

    def parseAjax(self, response, **kwargs):
        meta = response.meta
        # print(meta)
        results = json.loads(response.text)
        if (len(results['list']) > 0):
            item = DaniellespiderItem()
            item['title'] = results['list'][0]['bulletinName']
            item['bulletinIssueTime'] = results['list'][0]['bulletinIssueTime']
            item['source'] = meta['source']
            item['url'] = meta['detailUrl']
            item['sheetName'] = meta['sheetName']
            yield item
