import imp
import xlsxwriter
import json

from itemadapter import ItemAdapter

class XlsWriterPipeline:
    
    def open_spider(self, spider):
        self.workbook = xlsxwriter.Workbook('hello.xlsx')
        self.workbook.add_worksheet("招标信息汇总")
        self.workbook.add_worksheet("中标信息汇总")
        
    def close_spider(self, spider):
        self.workbook.close()

    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        print(adapter)
        return item
