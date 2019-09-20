# Author :  lncs
# Time:     2019-09-19 15:43
# File :    eastmoney_crawler.py
# Software: PyCharm

from selenium import webdriver
from bs4 import BeautifulSoup
import re
import pandas as pd
import time

from logpublic import *
from dbpublic import DbUtils


class morningstar_parse():
    def __init__(self, url):
        self.driver = webdriver.Chrome()
        self.url = url
        self.driver.get(self.url)
        time.sleep(5)

    def _get_total_record(self):
        data = self.driver.page_source
        bs = BeautifulSoup(data, 'lxml')
        span = bs.find_all('span', {'id': "ctl00_cphMain_TotalResultLabel"})
        total_record = span[0].string
        app_logger.info('共有记录:{}条'.format(total_record))

        return total_record

    def _get_fund_snapshot(self):
        """
        获取基金筛选页中快照信息
        :return:
            code_list-基金代码
            name_list-基金名称
            fund_type-基金类型
            fund_rate_3-三年评级等级
            fund_rate_5-五年评级等级
            net_value-单位净值(元)
            daily_change净值日变动(元)
            returns_curr_year-今年以来回报率(%)
        """
        app_logger.info('开始查询基金快照信息')
        code_list = []
        name_list = []
        fund_type = []
        fund_rate_3 = []
        fund_rate_5 = []
        net_value = []
        daily_change = []
        returns_curr_year = []

        # 获取每页的源代码
        data = self.driver.page_source
        if data == None:
            app_logger.warn('数据获取失败，重新获取...')
            time.sleep(30)
            data = self.driver.page_source
        bs = BeautifulSoup(data, 'lxml')

        # 数组在这两个类下面
        class_list = ['gridItem', 'gridAlternateItem']
        for i in range(len(class_list)):
            for tr in bs.find_all('tr', {'class': class_list[i]}):
                tds_text = tr.find_all('td', {'class': "msDataText"})
                tds_nume = tr.find_all('td', {'class': "msDataNumeric"})
                code_list.append(tds_text[0].find_all('a')[0].string)
                name_list.append(tds_text[1].find_all('a')[0].string)
                fund_type.append(tds_text[2].string)
                fund_rate_3.append(re.search('\d', tds_text[3].find_all('img')[0]['src']).group())
                fund_rate_5.append(re.search('\d', tds_text[4].find_all('img')[0]['src']).group())
                net_value.append(tds_nume[1].string)
                daily_change.append(tds_nume[2].string)
                returns_curr_year.append(tds_nume[3].string)
        for i in range(len(code_list)):
            app_logger.debug(
                '基金代码[{}],基金名称[{}],基金类型[{}],三年评级[{}],五年评级[{}],单位净值[{}],净值日变动[{}],今年以来回报[{}]'
                    .format(code_list[i], name_list[i], fund_type[i], fund_rate_3[i], fund_rate_5[i], net_value[i],
                            daily_change[i], returns_curr_year[i]))

        return code_list, name_list, fund_type, fund_rate_3, fund_rate_5, net_value, daily_change, returns_curr_year

    def _get_fund_portfolio(self):
        """
        获取基金的投资组合信息
        :return:
            code_list-基金代码
            stock_percent-股票仓位
            bond_percent-债券仓位
            top10_stock_percent-前十大持股
            top5_bond_percent-前五大债券
            net_asset-净资产
        """
        app_logger.info('开始查询基金投资组合信息')

        code_list = []
        stock_percent = []
        bond_percent = []
        top10_stock_percent = []
        top5_bond_percent = []
        net_asset = []
        # 获取每页的源代码
        data = self.driver.page_source
        if data == None:
            app_logger.warn('数据获取失败，重新获取...')
            time.sleep(30)
            data = self.driver.page_source
        bs = BeautifulSoup(data, 'lxml')

        # 数组在这两个类下面
        class_list = ['gridItem', 'gridAlternateItem']
        for i in range(len(class_list)):
            for tr in bs.find_all('tr', {'class': class_list[i]}):
                # if i == 0:
                #     print(tr)
                tds_text = tr.find_all('td', {'class': "msDataText"})
                tds_nume = tr.find_all('td', {'class': "msDataNumeric"})
                code_list.append(tds_text[0].find_all('a')[0].string)

                stock_percent.append(tds_nume[0].string)
                bond_percent.append(tds_nume[1].string)
                top10_stock_percent.append(tds_nume[2].string)
                top5_bond_percent.append(tds_nume[3].string)
                net_asset.append(tds_nume[4].string)

        for i in range(len(code_list)):
            app_logger.debug(
                '基金代码[{}],股票仓位[{}],债券仓位[{}],前十大持股[{}],前五大债券[{}],净资产[{}]'
                    .format(
                    code_list[i], stock_percent[i], bond_percent[i], top10_stock_percent[i], top5_bond_percent[i],
                    net_asset[i]))

        return code_list, stock_percent, bond_percent, top10_stock_percent, top5_bond_percent, net_asset

    def _get_fund_purchase_info(self):
        """
        获取基金筛选页中购买信息
        :return:
            code_list-基金代码
            name_list-基金名称
            foundation_date-成立日期
            subscribe_status-申购状态
            redeem_status-赎回状态
            initial_purchase_base-最小投资额(元)
            front_load_fee-前段收费(%)
            defer_load_fee-后端收费(%)
            redemption_fee-赎回费(%)
            management_fee-管理费(%)
            custodial_fee-托管费(%)
            distribution_fee-销售服务费(%)
        """
        app_logger.info('开始查询基金购买信息')
        code_list = []
        name_list = []
        foundation_date = []
        subscribe_status = []
        redeem_status = []
        initial_purchase_base = []
        front_load_fee = []
        defer_load_fee = []
        redemption_fee = []
        management_fee = []
        custodial_fee = []
        distribution_fee = []

        # 获取每页的源代码
        data = self.driver.page_source
        if data == None:
            app_logger.warn('数据获取失败，重新获取...')
            time.sleep(30)
            data = self.driver.page_source
        bs = BeautifulSoup(data, 'lxml')

        # 数组在这两个类下面
        class_list = ['gridItem', 'gridAlternateItem']
        for i in range(len(class_list)):
            for tr in bs.find_all('tr', {'class': class_list[i]}):
                # if i == 0:
                #     print(tr)
                tds_text = tr.find_all('td', {'class': "msDataText"})
                tds_nume = tr.find_all('td', {'class': "msDataNumeric"})
                code_list.append(tds_text[0].find_all('a')[0].string)
                name_list.append(tds_text[1].find_all('a')[0].string)

                foundation_date.append(tds_nume[0].string)
                subscribe_status.append(tds_nume[1].string)
                redeem_status.append(tds_nume[2].string)
                initial_purchase_base.append(tds_nume[3].string)
                front_load_fee.append(tds_nume[4].string)
                defer_load_fee.append(tds_nume[5].string)
                redemption_fee.append(tds_nume[6].string)
                management_fee.append(tds_nume[7].string)
                custodial_fee.append(tds_nume[8].string)
                distribution_fee.append(tds_nume[9].string)

        for i in range(len(code_list)):
            app_logger.debug(
                '基金代码[{}],基金名称[{}],成立日期[{}],申购状态[{}],赎回状态[{}],最小投资额(元)[{}],'
                '前段收费(%)[{}],后端收费(%)[{}],赎回费(%)[{}],管理费(%)[{}],托管费(%)[{}],销售服务费(%)[{}]'
                    .format(
                    code_list[i], name_list[i], foundation_date[i], subscribe_status[i], redeem_status[i],
                    initial_purchase_base[i], front_load_fee[i], defer_load_fee[i], redemption_fee[i],
                    management_fee[i], custodial_fee[i], distribution_fee[i]))

        return code_list, name_list, foundation_date, subscribe_status, redeem_status, initial_purchase_base, \
               front_load_fee, defer_load_fee, redemption_fee, management_fee, custodial_fee, distribution_fee

    def get_all_funds(self, request_page=None):
        # options = webdriver.ChromeOptions
        # prefs = {'profile.default_content_settings.popups': 0, "profile.default_content_setting_values.automatic_downloads": 1}
        # options.add_experimental_option('prefs', prefs)
        # driver = webdriver.Chrome(options=options)
        # driver = webdriver.Chrome()
        total_count = self._get_total_record()
        rows_per_page = 25

        time.sleep(5)
        if request_page != None:
            total_page = request_page
        else:
            total_page = int(total_count) // rows_per_page
        app_logger.info('需要查询[{}]页'.format(total_page))

        dbutils = DbUtils()

        page_num = 0
        while page_num < total_page:
            code_list, name_list, fund_type, fund_rate_3, fund_rate_5, net_value, daily_change, returns_curr_year = self._get_fund_snapshot()

            fund_df = pd.DataFrame(
                {'fund_code': code_list, 'fund_name': name_list, 'fund_type': fund_type, 'fund_rate_3': fund_rate_3,
                 'fund_rate_5': fund_rate_5, 'net_value': net_value, 'daily_change': daily_change,
                 'returns_curr_year': returns_curr_year})
            exec_sql = "insert ignore into  " \
                       "fund_morningstar(`fund_code`, `fund_name`,`fund_type`,`fund_rate_3`, `fund_rate_5`,`net_value`,`daily_change`,`returns_curr_year`)" \
                       " values (%s,%s,%s,%s,%s,%s,%s,%s)"
            fundinfo = fund_df.values.tolist()

            dbutils.execute_many(exec_sql, fundinfo)
            next_page = self.driver.find_element_by_link_text('>')
            next_page.click()
            page_num += 1

        self.driver.close()

    def get_select_funds(self, fund_name):

        data = self.driver.page_source
        bs = BeautifulSoup(data, 'lxml')
        # 选中三年评级三星及以上
        self.driver.find_element_by_id('ctl00_cphMain_cblStarRating_0').click()

        # 选中五年评级三星及以上
        self.driver.find_element_by_id('ctl00_cphMain_cblStarRating5_0').click()

        # 点击更多选型
        # span = bs.find_all('span', {'class': "msDataText"})
        self.driver.find_element_by_id('fs_moreoptions').click()

        # 输入基金名称
        self.driver.find_element_by_name('ctl00$cphMain$txtFund').click()
        self.driver.find_element_by_name('ctl00$cphMain$txtFund').send_keys(fund_name)
        time.sleep(2)

        # 点击查询
        self.driver.find_element_by_name('ctl00$cphMain$btnGo').click()

        total_count = self._get_total_record()
        rows_per_page = 25

        total_page = int(total_count) // rows_per_page + 1
        app_logger.info('需要查询[{}]页'.format(total_page))

        dbutils = DbUtils()
        # 先清空对应表
        dbutils.execute("truncate table fund_morningstar_select")

        page_num = 0
        # 查询快照信息
        while page_num < total_page:
            # 以上点击完成后点位页为【快照】
            code_list, name_list, fund_type, fund_rate_3, fund_rate_5, net_value, daily_change, returns_curr_year = self._get_fund_snapshot()

            fund_df = pd.DataFrame(
                {'fund_code': code_list, 'fund_name': name_list, 'fund_type': fund_type, 'fund_rate_3': fund_rate_3,
                 'fund_rate_5': fund_rate_5, 'net_value': net_value, 'daily_change': daily_change,
                 'returns_curr_year': returns_curr_year})
            exec_sql = "insert into  " \
                       "fund_morningstar_select(`fund_code`, `fund_name`,`fund_type`,`fund_rate_3`, `fund_rate_5`,`net_value`,`daily_change`,`returns_curr_year`)" \
                       " values (%s,%s,%s,%s,%s,%s,%s,%s)"
            fundinfo = fund_df.values.tolist()

            dbutils.execute_many(exec_sql, fundinfo)

            next_page = self.driver.find_element_by_link_text('>')
            next_page.click()
            page_num += 1

        time.sleep(5)
        # 查询购买信息，从起始页重新开始
        page_num = 0
        self.driver.find_element_by_link_text('<<').click()
        # 点击跳转到【购买信息】
        self.driver.find_element_by_id('ctl00_cphMain_lbOperations').click()
        while page_num < total_page:
            code_list, name_list, foundation_date, subscribe_status, redeem_status, initial_purchase_base, front_load_fee, defer_load_fee, redemption_fee, management_fee, custodial_fee, distribution_fee = self._get_fund_purchase_info()
            fund_df = pd.DataFrame(
                {
                    # 'fund_name': name_list,
                    'foundation_date': foundation_date,
                    'subscribe_status': subscribe_status,
                    'redeem_status': redeem_status,
                    'initial_purchase_base': initial_purchase_base,
                    'front_load_fee': front_load_fee,
                    'defer_load_fee': defer_load_fee,
                    'redemption_fee': redemption_fee,
                    'management_fee': management_fee,
                    'custodial_fee': custodial_fee,
                    'distribution_fee': distribution_fee,
                    'fund_code': code_list,
                }
            )
            exec_sql = "UPDATE fund_morningstar_select " \
                       "set `foundation_date` = %s, `subscribe_status` = %s, `redeem_status` = %s, " \
                       "`initial_purchase_base` = %s, `front_load_fee` = %s, `defer_load_fee` = %s, " \
                       "`redemption_fee` = %s, `management_fee` = %s, `custodial_fee` = %s, `distribution_fee` = %s " \
                       "where `fund_code` = %s"
            fundinfo = fund_df.values.tolist()

            dbutils.execute_many(exec_sql, fundinfo)

            next_page = self.driver.find_element_by_link_text('>')
            next_page.click()
            page_num += 1

        time.sleep(5)
        # 查询投资组合信息，从起始页重新开始
        page_num = 0
        self.driver.find_element_by_link_text('<<').click()
        # 点击跳转到【投资组合】
        self.driver.find_element_by_id('ctl00_cphMain_lbPortfolio').click()
        while page_num < total_page:
            code_list, stock_percent, bond_percent, top10_stock_percent, top5_bond_percent, net_asset = self._get_fund_portfolio()
            fund_df = pd.DataFrame(
                {
                    'stock_percent': stock_percent,
                    'bond_percent': bond_percent,
                    'top10_stock_percent': top10_stock_percent,
                    'top5_bond_percent': top5_bond_percent,
                    'net_asset': net_asset,
                    'fund_code': code_list,
                }
            )
            exec_sql = "UPDATE fund_morningstar_select " \
                       "set `stock_percent` = %s, `bond_percent` = %s, `top10_stock_percent` = %s, " \
                       "`top5_bond_percent` = %s, `net_asset` = %s " \
                       "where `fund_code` = %s"
            fundinfo = fund_df.values.tolist()

            dbutils.execute_many(exec_sql, fundinfo)

            next_page = self.driver.find_element_by_link_text('>')
            next_page.click()
            page_num += 1

        self.driver.close()


if __name__ == '__main__':
    url = "http://cn.morningstar.com/fundselect/default.aspx"
    # url = "http://cn.morningstar.com/quickrank/default.aspx"
    # get_page_info(url)
    msp = morningstar_parse(url)

    # 查询指定页数的基金信息，不指定参数为查询所有
    # msp.get_all_funds(5)

    # 模糊匹配基金名称
    msp.get_select_funds('沪深300')
