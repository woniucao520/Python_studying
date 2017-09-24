# coding=utf-8

import xlwt

import sys
reload(sys)
sys.setdefaultencoding('utf8')

class SaveBallDate(object):

    def __init__(self, items):
        self.items = items
        self.run(self.items)

    def run(self, items):
        fileName = u'result.xls'.encode('GBK')
        workbook = xlwt.Workbook()
        sheet = workbook.add_sheet(fileName,cell_overwrite_ok=True)
        title = [u'开奖日期', u'期号', u'中奖号码', u'销售额', u'一等奖', u'二等奖']
        for i, item in enumerate(title):
            sheet.write(0, i, item)

        i = 1
        while i <= len(items):
            item = items[i-1]
            sheet.write(i, 0, item.data)
            sheet.write(i, 1, item.order)
            sheet.write(i, 2, item.num)
            sheet.write(i, 3, item.money)
            sheet.write(i, 4, item.firstPrize)
            sheet.write(i, 5, item.secondPrize)
            i +=1
        workbook.save(fileName)



if __name__ == '__main__':
    pass

