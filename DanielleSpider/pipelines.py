# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import xlsxwriter

class DaniellespiderPipeline:
    def open_spider(self, spider):
        self.workbook = xlsxwriter.Workbook('hello.xlsx')
        self.workbook.add_worksheet("招标信息汇总")
        self.workbook.add_worksheet("中标信息汇总")
        self.countMap = {'招标信息汇总': 1, '中标信息汇总': 1}

    def close_spider(self, spider):
        self.workbook.close()

    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        sheetName = adapter['sheetName']
        sheet = self.workbook.get_worksheet_by_name(sheetName)
        count = self.countMap[sheetName]
        countStr = str(count)
        sheet.write('A'+countStr, adapter['source'])
        sheet.write('B'+countStr, adapter['bulletinIssueTime'])
        sheet.write('C'+countStr, adapter['title'])
        sheet.write('D'+countStr, adapter['url'])
        self.countMap[sheetName] = count + 1
        return item
