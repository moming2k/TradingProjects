#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @Filename: sh_bulk_bonds_trading_info
# @Date: 2017-02-22
# @Author: Mark Wang
# @Email: wangyouan@gmial.com


from sh_bulk_stock_trading_info import SHBulkStockTradingInfo


class SHBulkBondsTradingInfo(SHBulkStockTradingInfo):
    def init_constant(self):
        self.STOCK_ID = 'stockid'
        self.TRADE_DATE = 'tradedate'
        self.TRADE_VOLUME = 'tradeqty'
        self.BRANCH_SELL = 'branchsell'
        self.BRANCH_BUY = 'branchbuy'
        self.TRADE_PRICE = 'tradeprice'
        self.IS_SPECIAL = 'ifZc'
        self.TRADE_AMOUNT = 'tradeamount'
        self.SECURITY_NAME = 'abbrname'

        self.get_data_dict = {'jsonCallBack': 'jsonpCallback79256',
                              'isPagination': 'true',
                              'sqlId': 'COMMON_SSE_XXPL_JYXXPL_DZJYXX_L_2',
                              'stockId': '',
                              'startDate': '1990-01-01',
                              'endDate': '2017-02-22',
                              'pageHelp.pageSize': 25,
                              'pageHelp.pageNo': 1,
                              'pageHelp.beginPage': 1,
                              'pageHelp.endPage': 5,
                              'pageHelp.cacheSize': 1,
                              '_': 1487691935978, }

        self.start_date = '1990-01-01'
        self.end_date = ''
        self.failed_page_list = []


if __name__ == '__main__':
    import sys
    import logging
    import datetime

    save_name = 'sh_block_bonds_trading_report'

    logging.basicConfig(stream=sys.stdout, level=logging.DEBUG,
                        format='%(asctime)-15s %(name)s %(levelname)-8s: %(message)s')

    today_str = datetime.datetime.today().strftime('%Y%m%d')

    test = SHBulkBondsTradingInfo()

    result_df = test.download_report()
    result_df.to_pickle('{}_{}.p'.format(today_str, save_name))
    result_df.to_excel('{}_{}.xlsx'.format(today_str, save_name),
                       index=False)
