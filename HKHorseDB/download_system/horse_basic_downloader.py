#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @Filename: horse_basic_downloader
# @Date: 2017-02-13
# @Author: Mark Wang
# @Email: wangyouan@gmial.com

import time
import logging
from html.parser import HTMLParser

import pandas as pd
from bs4 import BeautifulSoup

from http_ctrl import HttpCtrl
from constants import Constant


class HorseBasicDownloader(Constant):
    def __init__(self, logger=None):
        if logger is None:
            self.logger = logging.getLogger(self.__class__.__name__)
            self.ctrl = HttpCtrl()

        else:
            self.logger = logger.getLogger(self.__class__.__name__)
            self.ctrl = HttpCtrl(logger)

    def download_horse_info(self):
        self.logger.info('Start to download all horse info')

        # Download horse name and id
        horse_id = self.__get_all_horse_name()

        # Download each horse information
        return self.__get_horse_detail_info(horse_id)

    def __get_all_horse_name(self):
        self.logger.info('Start to collect all horse name info')
        horse_info_list = []

        basic_url = 'http://{}/{}/{}'.format(self.HKJC_HOST_URL, self.ENGLISH, self.HORSE_LIST_PAGE)

        for i in range(26):
            current_char = chr(i + 65)
            current_url = '{}?ordertype={}'.format(basic_url, current_char)
            self.logger.debug('Get page {} info'.format(current_char))
            page_html = self.ctrl.get(current_url, headers={'Referer': current_url})
            horse_info_list.append(self.__decode_horse_list_page(page_html=page_html))
            time.sleep(3)

        self.logger.info('Collect horse name finished')
        return pd.concat(horse_info_list, axis=0, ignore_index=True).reset_index(drop=True)

    def __decode_horse_list_page(self, page_html):
        self.logger.debug('Start to decode page info')
        soup = BeautifulSoup(page_html)

        all_tables = soup.findAll('table')

        def is_horse_info_page(tb):
            a_list = tb.findAll('a')
            return len(a_list) == 1 and a_list[0].get('href').startswith('horse.asp')

        horse_info = pd.DataFrame(columns=[self.NAME, self.CODE])

        index = 0
        for table in all_tables:
            self.logger.debug('Table content: {}'.format(table))
            if not is_horse_info_page(table):
                continue
            # print table
            horse_code = table.findAll('a')[0].get('href').split('=')[-1]
            horse_name = table.findAll('a')[0].text
            horse_info.loc[index] = {self.NAME: horse_name,
                                     self.CODE: horse_code}
            index += 1

        return horse_info

    def __get_horse_detail_info(self, horse_id_df):
        columns = [self.SIRE, '{}{}'.format(self.TRAINER, self.CODE), self.ORIGIN, self.AGE, self.SEX, self.COLOR,
                   self.SEASON_STAKE, self.TOTAL_STAKE, self.NUMBER_ONE, self.NUMBER_STARTS, self.NUMBER_THREE,
                   self.NUMBER_TWO, '{}{}'.format(self.ENGLISH, self.OWNER), '{}{}'.format(self.CHINESE, self.OWNER),
                   '{}{}'.format(self.ENGLISH, self.NAME), '{}{}'.format(self.CHINESE, self.NAME),
                   self.CURRENT_RATING, self.SEASON_START_RATING, self.DAM, self.DAM_SIRE, self.IMPORT_TYPE]

        # horse_columns = map(lambda x: '{}{}'.format(self.HORSE, x), columns)
        # self.logger.debug('Columns: {}'.format(columns))
        horse_info_df = pd.DataFrame(columns=columns)
        self.logger.info('Start to query detail info of horse')

        for index in horse_id_df.index:
            horse_code = horse_id_df.ix[index, self.CODE]
            self.logger.debug('Horse code is {}'.format(horse_code))
            chinese_info = self.__get_horse_chinese_info(horse_code)

            english_info = self.__get_horse_english_info(horse_code)

            chinese_info.update(english_info)
            chinese_info['{}{}'.format(self.ENGLISH, self.NAME)] = horse_id_df.ix[index, self.NAME]
            # self.logger.debug('Saved data info: {}'.format(chinese_info))
            horse_info_df.loc[horse_code] = chinese_info
            time.sleep(3)

        self.logger.info('Query detail info of horse finished')
        result_df = pd.DataFrame(index=horse_info_df.index)
        for column in horse_info_df.keys():
            result_df['{}{}'.format(self.HORSE, column)] = horse_info_df[column]

        return result_df

    def download_horse_id_list(self, horse_id_list):
        columns = [self.SIRE, '{}{}'.format(self.TRAINER, self.CODE), self.ORIGIN, self.AGE, self.SEX, self.COLOR,
                   self.SEASON_STAKE, self.TOTAL_STAKE, self.NUMBER_ONE, self.NUMBER_STARTS, self.NUMBER_THREE,
                   self.NUMBER_TWO, '{}{}'.format(self.ENGLISH, self.OWNER), '{}{}'.format(self.CHINESE, self.OWNER),
                   '{}{}'.format(self.ENGLISH, self.NAME), '{}{}'.format(self.CHINESE, self.NAME),
                   self.CURRENT_RATING, self.SEASON_START_RATING, self.DAM, self.DAM_SIRE, self.IMPORT_TYPE]

        # horse_columns = map(lambda x: '{}{}'.format(self.HORSE, x), columns)
        # self.logger.debug('Columns: {}'.format(columns))
        horse_info_df = pd.DataFrame(columns=columns)
        self.logger.info('Start to query detail info of horse')

        for horse_code in horse_id_list:
            self.logger.debug('Horse code is {}'.format(horse_code))
            chinese_info = self.__get_horse_chinese_info(horse_code)

            english_info = self.__get_horse_english_info(horse_code)

            chinese_info.update(english_info)
            chinese_info['{}{}'.format(self.ENGLISH, self.NAME)] = ''
            # self.logger.debug('Saved data info: {}'.format(chinese_info))
            horse_info_df.loc[horse_code] = chinese_info
            time.sleep(1)

        self.logger.info('Query detail info of horse finished')
        result_df = pd.DataFrame(index=horse_info_df.index)
        for column in horse_info_df.keys():
            result_df['{}{}'.format(self.HORSE, column)] = horse_info_df[column]

        return result_df

    def __get_horse_chinese_info(self, horse_code):
        self.logger.info('Get Chinese detail of horse code {}'.format(horse_code))
        query_url = '{}/{}/{}/{}'.format(self.HKJC_RACING_URL, self.HORSE_DETAIL_PAGE, self.CHINESE, horse_code)
        page_info = self.ctrl.get(query_url)
        soup = BeautifulSoup(page_info)
        name = soup.title.text.split(' - ')[0]
        owner_name = soup.findAll('table')[2].findAll('tr')[1].findAll('a')[0].text
        return {'{}{}'.format(self.CHINESE, self.NAME): name,
                '{}{}'.format(self.CHINESE, self.OWNER): owner_name}

    def __get_horse_english_info(self, horse_code):
        self.logger.info('Get English detail of horse code {}'.format(horse_code))
        query_url = '{}/{}/{}/{}'.format(self.HKJC_RACING_URL, self.HORSE_DETAIL_PAGE, self.ENGLISH, horse_code)
        page_info = self.ctrl.get(query_url)

        soup = BeautifulSoup(page_info)
        h = HTMLParser()

        table1 = soup.findAll('table')[1]
        table2 = soup.findAll('table')[2]

        result_dict = {
            '{}{}'.format(self.ENGLISH, self.OWNER): table2.findAll('tr')[1].findAll('a')[0].text,
            self.IMPORT_TYPE: table1.findAll('tr')[2].find('td').text,
            self.SEASON_STAKE: table1.findAll('tr')[3].find('td').text,
            self.TOTAL_STAKE: table1.findAll('tr')[4].find('td').text,
            '{}{}'.format(self.TRAINER, self.CODE): table2.findAll('tr')[0].find('a').get('href').split('=')[-1],
            self.CURRENT_RATING: table2.findAll('tr')[2].find('td').text,
            self.SEASON_START_RATING: table2.findAll('tr')[3].find('td').text,
            self.SIRE: table2.findAll('tr')[4].find('td').text,
            self.DAM: table2.findAll('tr')[5].find('td').text,
            self.DAM_SIRE: table2.findAll('tr')[6].find('td').text,
        }

        country_age = h.unescape(table1.findAll('tr')[0].find('td').text).split('/')
        result_dict[self.ORIGIN] = country_age[0].replace(u'\xa0', u'')
        result_dict[self.AGE] = country_age[1].replace(u'\xa0', u'')

        color_sex = h.unescape(table1.findAll('tr')[1].find('td').text).split('/')
        result_dict[self.COLOR] = color_sex[0].replace(u'\xa0', u'')
        result_dict[self.SEX] = color_sex[1].replace(u'\xa0', u'')

        racing_info = table1.findAll('tr')[5].find('td').text.split('-')
        result_dict[self.NUMBER_THREE] = racing_info[2]
        result_dict[self.NUMBER_TWO] = racing_info[1]
        result_dict[self.NUMBER_ONE] = racing_info[0]
        result_dict[self.NUMBER_STARTS] = racing_info[3]

        return result_dict


if __name__ == '__main__':
    import sys

    logging.basicConfig(stream=sys.stdout, level=logging.INFO,
                        format='%(asctime)-15s %(name)s %(levelname)-8s: %(message)s')

    test = HorseBasicDownloader()

    # horse_basic_info = test.download_horse_info()
    # horse_basic_info.to_pickle('horse_info.p')
    # horse_basic_info.to_excel('horse_info.xlsx')

    target_id_list = [
        u'K411', u'S209', u'S186', u'S325', u'T130', u'M152', u'T182', u'S314', u'K118', u'G300', u'J329', u'G018',
        u'H167', u'K288', u'J237', u'L190', u'J123', u'K104', u'L304', u'K089', u'L253', u'M291', u'M365', u'L189',
        u'K215', u'K256', u'M406', u'M244', u'M155', u'J051', u'H286', u'V201', u'J014', u'H076', u'K057', u'H294',
        u'L030', u'L397', u'K389', u'E293', u'G261', u'K067', u'H053', u'L263', u'S224', u'P015', u'P223', u'P402',
        u'N027', u'L396', u'J131', u'P379', u'P203', u'P321', u'N327', u'P376', u'M250', u'M382', u'M161', u'M391',
        u'L308', u'K275', u'N272', u'G177', u'J181', u'J056', u'E139', u'K043', u'D322', u'E268', u'G040', u'G056',
        u'J171', u'K125', u'H122', u'N054', u'K212', u'J173', u'K202', u'N013', u'N076', u'K101', u'M167', u'M398',
        u'N313', u'M404', u'H316', u'M390', u'M331', u'M094', u'L341', u'M279', u'J293', u'L171', u'J217', u'J320',
        u'L406', u'M202', u'L121', u'K105', u'K295', u'L029', u'E275', u'G287', u'J250', u'K380', u'K401', u'J040',
        u'K062', u'K354', u'T291', u'P283', u'N392', u'N157', u'N423', u'S316', u'G141', u'G137', u'G010', u'D162',
        u'H019', u'J028', u'H078', u'G140', u'C298', u'J029', u'K344', u'G313', u'H261', u'C299', u'K253', u'H327',
        u'G213', u'K013', u'K042', u'K303', u'K359', u'K368', u'J174', u'G246', u'C024', u'CB105', u'E305', u'C238',
        u'E066', u'G127', u'D096', u'H273', u'H140', u'T161', u'S262', u'P018', u'N040', u'N333', u'P416', u'P258',
        u'K188', u'M384', u'L379', u'L213', u'N271', u'K164', u'L206', u'H284', u'N346', u'S160', u'M299', u'K360',
        u'P081', u'J059', u'L408', u'M191', u'L258', u'L133', u'M030', u'L281', u'P011', u'J020', u'L113', u'K014',
        u'K326', u'J304', u'J031', u'L067', u'J018', u'M229', u'M149', u'L209', u'M376', u'K066', u'M090', u'M274',
        u'N148', u'H302', u'N295', u'N231', u'N362', u'N155', u'M065', u'N292', u'P149', u'L343', u'M298', u'L394',
        u'N086', u'N051', u'N182', u'M056', u'N413', u'M338', u'N219', u'P378', u'M400', u'N211', u'N066', u'P177',
        u'L357', u'P019', u'P024', u'L324', u'N384', u'N296', u'N212', u'M192', u'M399', u'M228', u'P095', u'M131',
        u'P317', u'P112', u'S256', u'M199', u'S239', u'T316', u'T081', u'J111', u'K132', u'L220', u'N100', u'L373',
        u'L023', u'L178', u'L211', u'L254', u'L401', u'K373', u'S076', u'P281', u'P200', u'T271', u'N316', u'M245',
        u'N110', u'M174', u'N035', u'P071', u'P316', u'P271', u'J145', u'P052', u'P367', u'N436', u'L409', u'M112',
        u'K002', u'M235', u'N167', u'H262', u'L065', u'S445', u'N134', u'P308', u'N055', u'T072', u'S086', u'T328',
        u'P140', u'P178', u'P301', u'S403', u'P282', u'S392', u'M213', u'J265', u'M055', u'L106', u'L161', u'K169',
        u'M126', u'L230', u'M067', u'L085', u'K307', u'L013', u'H069', u'L302', u'H214', u'J284', u'K309', u'J333',
        u'L276', u'E179', u'H042', u'G074', u'G163', u'H244', u'G094', u'E251', u'C370', u'H118', u'G032', u'H054',
        u'G134', u'D194', u'M176', u'M117', u'M200', u'M342', u'M066', u'M004', u'J297', u'N118', u'P127', u'P238',
        u'N394', u'P067', u'N282', u'N053', u'N266', u'N097', u'P315', u'P029', u'N307', u'S011', u'P349', u'P343',
        u'T111', u'L222', u'K001', u'J019', u'K176', u'G183', u'K318', u'K395', u'M144', u'J263', u'J143', u'J011',
        u'J203', u'H235', u'J039', u'L278', u'K342', u'H071', u'L366', u'L155', u'M034', u'J003', u'J346', u'K050',
        u'H025', u'H153', u'H285', u'J312', u'H232', u'L137', u'J095', u'N196', u'M158', u'K205', u'P306', u'M074',
        u'P167', u'M013', u'M064', u'M247', u'K223', u'K026', u'J134', u'K406', u'M063', u'J074', u'P174', u'N012',
        u'M207', u'K231', u'P176', u'E244', u'E049', u'H280', u'K160', u'K159', u'J243', u'K078', u'J342', u'K025',
        u'P145', u'L100', u'K210', u'L277', u'K247', u'K199', u'L048', u'D250', u'L032', u'H143', u'L092', u'J196',
        u'L420', u'S155', u'S412', u'P153', u'M058', u'L183', u'M329', u'M231', u'L368', u'M307', u'L197', u'L380',
        u'M334', u'M239', u'K029', u'K377', u'L036', u'K130', u'M328', u'M041', u'L186', u'L431', u'M107', u'L212',
        u'M151', u'N107', u'L332', u'J038', u'H257', u'J117', u'H180', u'J055', u'D226', u'H021', u'G158', u'H202',
        u'H204', u'H117', u'J022', u'N448', u'P180', u'N142', u'M226', u'S081', u'M111', u'N303', u'M026', u'T257',
        u'H331', u'N220', u'N189', u'K398', u'N002', u'M361', u'N127', u'N439', u'N306', u'L151', u'L034', u'L393',
        u'J257', u'K245', u'K397', u'P227', u'P285', u'S290', u'S035', u'S114', u'M099', u'L326', u'M129', u'L160',
        u'M005', u'L435', u'E050', u'J070', u'V097', u'H023', u'CB177', u'H044', u'C198', u'E167', u'N255', u'N264',
        u'N388', u'P139', u'T127', u'N140', u'P146', u'P152', u'P262', u'K284', u'K214', u'G212', u'L019', u'J301',
        u'H253', u'G233', u'H246', u'L274', u'L045', u'L426', u'M263', u'P033', u'K340', u'M054', u'N057', u'L333',
        u'N047', u'T231', u'S192', u'P280', u'N335', u'P163', u'L158', u'P101', u'S002', u'M010', u'P028', u'N301',
        u'P084', u'M162', u'J308', u'L134', u'N183', u'L153', u'M272', u'N033', u'P273', u'N369', u'N446', u'N356',
        u'K218', u'N113', u'N209', u'P117', u'N438', u'J303', u'J315', u'G274', u'J213', u'H017', u'K293', u'H026',
        u'L378', u'J138', u'K139', u'K292', u'M135', u'J199', u'K123', u'K065', u'L110', u'M060', u'J161', u'N370',
        u'N084', u'N412', u'S182', u'P219', u'P062', u'L136', u'M405', u'M381', u'M367', u'M296', u'J090', u'L352',
        u'N141', u'N218', u'M332', u'S136', u'S157', u'N402', u'J160', u'M387', u'M150', u'L227', u'M160', u'N149',
        u'P277', u'P042', u'N223', u'P061', u'P181', u'M393', u'P443', u'P016', u'M326', u'S336', u'J351', u'H276',
        u'H096', u'K073', u'K300', u'K386', u'K347', u'H168', u'G270', u'H092', u'K182', u'J184', u'H314', u'K181',
        u'H320', u'H222', u'H097', u'J328', u'P032', u'L268', u'K134', u'J114', u'K162', u'L112', u'J177', u'L014',
        u'J280', u'K137', u'K266', u'K186', u'J242', u'J082', u'J034', u'L175', u'E052', u'H150', u'J310', u'E155',
        u'K285', u'H299', u'J190', u'G159', u'L187', u'J226', u'H116', u'K187', u'J165', u'H081', u'J289', u'K191',
        u'H278', u'J066', u'J228', u'L363', u'P299', u'P171', u'N262', u'T058', u'P058', u'S257', u'P183', u'N344',
        u'P446', u'P038', u'L342', u'P035', u'P291', u'N028', u'L290', u'P175', u'N099', u'H290', u'D130', u'G298',
        u'G234', u'E125', u'E126', u'J294', u'H034', u'G079', u'H198', u'J036', u'H029', u'D378', u'E301', u'M366',
        u'K149', u'L074', u'M086', u'K327', u'K304', u'M119', u'N048', u'D019', u'C003', u'H113', u'J204', u'G110',
        u'J102', u'G165', u'H175', u'J180', u'D009', u'H037', u'H008', u'E225', u'H132', u'C181', u'J026', u'G073',
        u'H137', u'M137', u'K376', u'M212', u'M395', u'M269', u'G169', u'J099', u'K055', u'K070', u'J101', u'K075',
        u'H154', u'G157', u'H234', u'G294', u'E159', u'C214', u'E042', u'H041', u'J072', u'H065', u'S237', u'P344',
        u'T296', u'S165', u'T044', u'N088', u'K145', u'K004', u'N428', u'L016', u'N304', u'K091', u'N374', u'M113',
        u'J262', u'M278', u'M415', u'L376', u'L088', u'M293', u'M302', u'K358', u'M287', u'K410', u'L174', u'K036',
        u'L139', u'L172', u'K136', u'H240', u'D397', u'H301', u'G223', u'J042', u'T365', u'S340', u'T172', u'T158',
        u'J352', u'E106', u'H268', u'E147', u'J175', u'D165', u'G027', u'P001', u'N254', u'T128', u'P241', u'K163',
        u'K405', u'K085', u'L049', u'L188', u'K323', u'K349', u'K311', u'K278', u'J132', u'N371', u'M035', u'L260',
        u'N385', u'K170', u'K315', u'L097', u'H242', u'H197', u'H317', u'G217', u'J107', u'H043', u'K039', u'J216',
        u'D084', u'H321', u'P025', u'L338', u'N326', u'M318', u'K383', u'P441', u'P318', u'P119', u'T354', u'N046',
        u'M252', u'P304', u'P074', u'L369', u'M036', u'P260', u'P017', u'N146', u'P075', u'M061', u'E070', u'J230',
        u'E100', u'G250', u'J141', u'H293', u'H095', u'M300', u'L033', u'L413', u'H187', u'G304', u'H108', u'D274',
        u'G041', u'H251', u'G037', u'P412', u'N138', u'P254', u'L192', u'P385', u'N226', u'S273', u'M227', u'S003',
        u'N427', u'K116', u'G033', u'H004', u'H296', u'J087', u'K058', u'K120', u'S062', u'M377', u'P122', u'N257',
        u'N101', u'P103', u'C342', u'G004', u'E132', u'G264', u'J061', u'D336', u'E072', u'E255', u'G049', u'L021',
        u'H195', u'K325', u'L349', u'K348', u'M412', u'L306', u'P305', u'N200', u'J079', u'H210', u'H163', u'J220',
        u'K222', u'G320', u'L041', u'G308', u'H082', u'H312', u'J182', u'C015', u'G143', u'E172', u'J151', u'T297',
        u'H127', u'J167', u'E187', u'E250', u'E062', u'CB300', u'D261', u'P417', u'N238', u'N024', u'D213', u'K267',
        u'K194', u'L251', u'L386', u'M388', u'L241', u'M297', u'L424', u'P334', u'S255', u'M021', u'S102', u'S041',
        u'D080', u'H040', u'K138', u'G161', u'J142', u'E031', u'E198', u'D238', u'K168', u'K007', u'J221', u'C213',
        u'J152', u'K024', u'K031', u'E224', u'L252', u'M305', u'M261', u'P086', u'K353', u'L104', u'L384', u'K016',
        u'L383', u'S134', u'P082', u'S292', u'N445', u'P371', u'L098', u'N075', u'M182', u'N128', u'S270', u'P395',
        u'P428', u'N098', u'N253', u'M284', u'N112', u'N168', u'K393', u'E143', u'E287', u'D234', u'N175', u'L399',
        u'K226', u'M098', u'M343', u'N120', u'M314', u'P197', u'P387', u'P213', u'M373', u'N185', u'L009', u'P096',
        u'S187', u'P198', u'N188', u'P408', u'N090', u'S307', u'P229', u'P289', u'N407', u'T307', u'S395', u'T137',
        u'K390', u'N201', u'M195', u'M251', u'M268', u'T155', u'J124', u'K362', u'K102', u'K133', u'E124', u'K110',
        u'H330', u'K329', u'K044', u'V067', u'T086', u'T020', u'S444', u'S408', u'S252', u'S144', u'P404', u'S330',
        u'L063', u'L382', u'L310', u'M084', u'M165', u'H048', u'N323', u'S353', u'T144', u'M096', u'N007', u'M341',
        u'N259', u'L370', u'H239', u'M259', u'M197', u'L185', u'K147', u'K094', u'K154', u'J098', u'H015', u'H130',
        u'J037', u'J092', u'L150', u'N337', u'S025', u'P374', u'G117', u'H300', u'J033', u'J080', u'J136', u'J068',
        u'L286', u'L242', u'G178', u'L081', u'L132', u'K117', u'H112', u'J248', u'P298', u'M127', u'N202', u'L146',
        u'P292', u'P115', u'N279', u'L199', u'E181', u'D377', u'C099', u'H006', u'G202', u'E134', u'G279', u'H215',
        u'J231', u'J045', u'G095', u'N345', u'M322', u'K346', u'L031', u'L005', u'M335', u'T061', u'P216', u'D355',
        u'J135', u'E105', u'H292', u'N419', u'M118', u'L367', u'M330', u'L167', u'M256', u'L229', u'D301', u'CB327',
        u'D073', u'CB326', u'D118', u'E138', u'N217', u'P093', u'M193', u'S119', u'N229', u'N435', u'N314', u'N216',
        u'M211', u'S038', u'N386', u'G275', u'J073', u'E326', u'J023', u'S026', u'N396', u'S243', u'S097', u'P449',
        u'P426', u'P430', u'H103', u'H107', u'J085', u'C355', u'E068', u'J001', u'S108', u'M350', u'K189', u'L142',
        u'D199', u'J332', u'J282', u'N318', u'S103', u'L391', u'P266', u'N105', u'N115', u'S381', u'P401', u'T035',
        u'H318', u'H089', u'J212', u'J109', u'L385', u'L004', u'K224', u'P072', u'P325', u'N245', u'P055', u'L266',
        u'L042', u'H126', u'L232', u'K173', u'N004', u'N184', u'L207', u'P114', u'N302', u'T238', u'P169', u'P224',
        u'P222', u'N275', u'J137', u'K184', u'J198', u'L236', u'K097', u'K216', u'N135', u'P147', u'M201', u'P249',
        u'P261', u'H319', u'L425', u'K213', u'K074', u'L422', u'K272', u'K021', u'L028', u'L147', u'J225', u'K020',
        u'G020', u'G220', u'G111', u'G201', u'H087', u'J100', u'L002', u'L381', u'J340', u'J077', u'H231', u'H016',
        u'S306', u'N021', u'K230', u'M311', u'M410', u'L261', u'L040', u'L082', u'M100', u'N014', u'P134', u'T191',
        u'T037', u'N389', u'P053', u'L423', u'M266', u'K388', u'M095', u'H182', u'J306', u'L064', u'K341', u'L059',
        u'J125', u'E238', u'G307', u'H083', u'H315', u'J200', u'K037', u'D330', u'H094', u'J191', u'E289', u'G317',
        u'G312', u'D300', u'M383', u'N324', u'P170', u'N102', u'P211', u'P209', u'K238', u'L079', u'K221', u'K046',
        u'H192', u'K040', u'P444', u'V005', u'P242', u'T069', u'L094', u'M357', u'G131', u'J326', u'H205', u'H128',
        u'L024', u'L347', u'T304', u'K316', u'M173', u'M136', u'M183', u'M046', u'L272', u'T014', u'V383', u'G315',
        u'D308', u'L371', u'L404', u'L138', u'P383', u'P057', u'P340', u'L195', u'M358', u'S058', u'L428', u'S236',
        u'S194', u'P008', u'M280', u'N019', u'M214', u'N003', u'K399', u'J168', u'K352', u'K351', u'L105', u'P116',
        u'S046', u'P389', u'G029', u'L283', u'L358', u'K289', u'L012', u'L273', u'L070', u'K093', u'V043', u'M043',
        u'K274', u'E257', u'H151', u'J162', u'G314', u'E291', u'E014', u'G125', u'C333', u'CB088', u'G135', u'S448',
        u'J281', u'C066', u'CB125', u'J146', u'M206', u'M087', u'N270', u'N398', u'H226', u'J096', u'G247', u'G311',
        u'G055', u'G152', u'S004', u'S091', u'N429', u'J337', u'N222', u'E045', u'K155', u'K264', u'J069', u'K034',
        u'E209', u'H208', u'H203', u'J239', u'K265', u'T121', u'G123', u'CB406', u'E311', u'E324', u'J006', u'G122',
        u'V004', u'M007', u'K297', u'K324', u'G251', u'E263', u'N143', u'S369', u'S006', u'N070', u'P397', u'M057',
        u'P184', u'S215', u'S434', u'G180', u'L181', u'L006', u'K072', u'H282', u'D071', u'L317', u'P054', u'M224',
        u'N330', u'M374', u'N274', u'N037', u'P296', u'HK$', u'P034', u'M120', u'P132', u'H258', u'N288', u'P225',
        u'N399', u'S327', u'N403', u'M267', u'T398', u'P102', u'M378', u'N401', u'D083', u'CA115', u'E332', u'C223',
        u'J158', u'S313', u'S066', u'K367', u'L010', u'L101', u'M281', u'N096', u'M181', u'M124', u'H145', u'E333',
        u'H306', u'H169', u'E254', u'G265', u'D239', u'M222', u'M407', u'M283', u'M215', u'H212', u'G281', u'H058',
        u'E300', u'J187', u'J311', u'P382', u'N165', u'K237', u'E055', u'J300', u'J264', u'K294', u'L416', u'L054',
        u'M262', u'J268', u'L086', u'K111', u'M396', u'E205', u'H129', u'E327', u'H064', u'S357', u'L364', u'K054',
        u'L298', u'H281', u'K291', u'K109', u'E270', u'L204', u'L169', u'L140', u'L355', u'N322', u'L177', u'S415',
        u'P411', u'T212', u'L076', u'M356', u'N414', u'L418', u'N234', u'K308', u'K313', u'J192', u'D207', u'K006',
        u'J194', u'G145', u'J246', u'N379', u'N400', u'M347', u'M039', u'K287', u'L243', u'S170', u'N325', u'M386',
        u'H271', u'E207', u'J105', u'G170', u'H124', u'H247', u'K334', u'K041', u'K276', u'J169', u'N015', u'N420',
        u'P331', u'P347', u'S092', u'M241', u'N043', u'H259', u'P118', u'P246', u'M246', u'P345', u'N299', u'K077',
        u'S122', u'L275', u'M234', u'L235', u'E183', u'K220', u'L118', u'K403', u'L214', u'K407', u'P228', u'P234',
        u'S085', u'S293', u'N291', u'S360', u'G006', u'E262', u'E247', u'L018', u'L071', u'M133', u'L196', u'K335',
        u'K270', u'K394', u'G077', u'CA018', u'G118', u'G235', u'E127', u'S308', u'M080', u'N161', u'N061', u'L193',
        u'L025', u'K260', u'K035', u'L027', u'K338', u'K177', u'H046', u'M178', u'L173', u'N119', u'M121', u'L372',
        u'P124', u'L240', u'T208', u'T225', u'T016', u'P424', u'S049', u'M019', u'E193', u'E040', u'H166', u'P398',
        u'L095', u'L221', u'S053', u'S137', u'S228', u'K387', u'M175', u'M031', u'L390', u'C089', u'H233', u'G291',
        u'G289', u'G017', u'H160', u'H009', u'M236', u'G182', u'H136', u'H305', u'H272', u'H211', u'J245', u'C368',
        u'P079', u'P410', u'T053', u'L056', u'L293', u'P026', u'J178', u'J305', u'J157', u'P148', u'P253', u'J255',
        u'L077', u'J319', u'H057', u'L238', u'J325', u'J170', u'L429', u'M089', u'M081', u'M024', u'N001', u'K023',
        u'G219', u'J189', u'J205', u'J035', u'H328', u'D323', u'E281', u'E256', u'G026', u'E033', u'CB189', u'K019',
        u'L392', u'L037', u'J032', u'E221', u'T013', u'S359', u'P199', u'E169', u'J154', u'E200', u'H036', u'J172',
        u'K107', u'K032', u'K086', u'J195', u'K280', u'J348', u'M294', u'L096', u'P384', u'P173', u'H002', u'K183',
        u'T126', u'P351', u'M223', u'L078', u'G120', u'K180', u'K369', u'G194', u'T101', u'M077', u'N240', u'L145',
        u'S198', u'N310', u'S188', u'K319', u'M379', u'S296', u'M292', u'L107', u'T260', u'S368', u'N250', u'N025',
        u'N079', u'N164', u'H313', u'H289', u'L297', u'K370', u'M233', u'N353', u'M188', u'J307', u'J052', u'K299',
        u'M243', u'M345', u'M221', u'M170', u'M185', u'K151', u'J256', u'J271', u'P155', u'H288', u'M145', u'N311',
        u'M205', u'N104', u'J240', u'K045', u'J179', u'K112', u'L201', u'K087', u'J232', u'K330', u'L296', u'L330',
        u'S238', u'P110', u'S222', u'T038', u'T006', u'S079', u'N224', u'E178', u'G045', u'G276', u'D271', u'G230',
        u'G044', u'E217', u'E285', u'H297', u'L103', u'G024', u'L387', u'J341', u'G060', u'K174', u'J322', u'J283',
        u'J113', u'H138', u'J339', u'J353', u'J244', u'L007', u'K385', u'E095', u'L255', u'J078', u'J278', u'L217',
        u'M079', u'E030', u'N087', u'L289', u'M163', u'H099', u'J207', u'H067', u'G216', u'C244', u'L264', u'N194',
        u'P323', u'P418', u'S302', u'S075', u'P433', u'S197', u'T115', u'L344', u'K396', u'L061', u'M323', u'N029',
        u'V218', u'J275', u'J133', u'N380', u'M315', u'L157', u'J047', u'L215', u'L434', u'L339', u'E258', u'G266',
        u'N366', u'N130', u'L060', u'M083', u'J296', u'M016', u'S175', u'L320', u'L403', u'L412', u'M101', u'S310',
        u'N151', u'M394', u'N391', u'N227', u'C029', u'E107', u'D256', u'H147', u'J215', u'J338', u'K178', u'H056',
        u'G257', u'CB249', u'H164', u'H178', u'H309', u'P364', u'H007', u'J227', u'T404', u'K156', u'G254', u'K251',
        u'M102', u'P264', u'L099', u'K248', u'K239', u'M017', u'M123', u'M194', u'H171', u'G078', u'E071', u'G263',
        u'T310', u'K060', u'K068', u'L075', u'P409', u'H184', u'L141', u'N071', u'CA381', u'J086', u'J024', u'T214',
        u'S363', u'K242', u'V033', u'H324', u'P366', u'N005', u'P089', u'P073', u'P078', u'M360', u'N261', u'S149',
        u'S375', u'P432', u'P135', u'H295', u'E047', u'E080', u'J004', u'E170', u'S123', u'S090', u'L179', u'K381',
        u'L093', u'N383', u'N233', u'L208', u'K375', u'L271', u'L348', u'K207', u'C068', u'J285', u'G260', u'D317',
        u'K027', u'C340', u'J058', u'S031', u'P240', u'N179', u'D205', u'H170', u'G084', u'N359', u'S233', u'S287',
        u'L203', u'M105', u'M264', u'E140', u'G295', u'D293', u'D351', u'G187', u'N276', u'M364', u'N239', u'L108',
        u'M248', u'P100', u'N397', u'N297', u'S350', u'M012', u'P131', u'P243', u'L001', u'K321', u'K017', u'J272',
        u'S190', u'N300', u'L129', u'L433', u'G098', u'H080', u'K121', u'K153', u'J150', u'J295', u'K175', u'M068',
        u'N372', u'M070', u'G310', u'D353', u'G057', u'S161', u'N408', u'K333', u'K279', u'J345', u'J321', u'K167',
        u'S099', u'T222', u'K233', u'T252', u'G072', u'J144', u'J089', u'J224', u'N176', u'L377', u'K064', u'L301',
        u'K193', u'L035', u'L375', u'H267', u'K361', u'E175', u'L069', u'H146', u'G104', u'J015', u'J081', u'G196',
        u'H266', u'D052', u'E008', u'T003', u'N331', u'P338', u'G146', u'C208', u'N320', u'K296', u'P006', u'S174',
        u'D069', u'CB320', u'L087', u'N137', u'M316', u'K320', u'N050', u'J236', u'M029', u'M009', u'M290', u'M265',
        u'N393', u'K268', u'K146', u'H191', u'CB368', u'C221', u'G046', u'P191', u'G050', u'H032', u'J147', u'N424',
        u'K302', u'L262', u'S394', u'M303', u'L228', u'N312', u'P051', u'N094', u'M242', u'L322', u'M042', u'M258',
        u'N252', u'K103', u'H049', u'K084', u'V262', u'M048', u'P239', u'N093', u'K157', u'K211', u'L102', u'G297',
        u'P157', u'M128', u'S171', u'G198', u'N243', u'N215', u'N198', u'N207', u'D248', u'L249', u'P172', u'S177',
        u'P414', u'N129', u'T012', u'N235', u'P196', u'N434', u'P091', u'T139', u'P350', u'S126', u'S071', u'S057',
        u'T060', u'J260', u'K328', u'H265', u'J064', u'S052', u'P399', u'M238', u'H221', u'N180', u'N052', u'N091',
        u'L191', u'N160', u'P013', u'L359', u'H183', u'T040', u'L282', u'G226', u'N116', u'M237', u'N089', u'M220',
        u'M156', u'M285', u'L083', u'N078', u'P037', u'P450', u'K249', u'M346', u'N422', u'P161', u'S141', u'N010',
        u'S067', u'T240', u'S400', u'N263', u'S214', u'P369', u'M071', u'L398', u'L291', u'M154', u'G068', u'K141',
        u'L405', u'M232', u'K305', u'L084', u'S311', u'N085', u'N251', u'P237', u'D230', u'G112', u'J049', u'J210',
        u'H269', u'J112', u'H274', u'K201', u'G232', u'M370', u'E012', u'J097', u'G262', u'M409', u'K261', u'L318',
        u'K100', u'J127', u'J335', u'M385', u'M115', u'L124', u'N260', u'N030', u'M210', u'K150', u'K301', u'J084',
        u'G105', u'P353', u'J186', u'K092', u'J017', u'K258', u'J005', u'D021', u'S365', u'J126', u'G106', u'N092',
        u'J071', u'M286', u'P160', u'P010', u'G269', u'J276', u'S018', u'L248', u'S056', u'M008', u'N191', u'K028',
        u'J176', u'C319', u'G003', u'E306', u'H179', u'L432', u'E288', u'J106', u'G309', u'L122', u'M354', u'L091',
        u'G243', u'K115', u'D388', u'G293', u'D335', u'H020', u'L345', u'M308', u'M134', u'P003', u'L003', u'K190',
        u'K244', u'L365', u'S153', u'S384', u'S059', u'S421', u'M217', u'P381', u'N016', u'N378', u'N172', u'N174',
        u'K209', u'J273', u'K080', u'K192', u'P440', u'S387', u'L205', u'P437', u'S140', u'N213', u'J327', u'M104',
        u'T085', u'N133', u'M408', u'N349', u'M038', u'L244', u'L374', u'L356', u'H050', u'T048', u'P080', u'S094',
        u'S068', u'K009', u'J247', u'K378', u'P165', u'H279', u'J012', u'V194', u'S048', u'N171', u'L247', u'T317',
        u'L267', u'P302', u'N073', u'J254', u'M309', u'N031', u'K371', u'E279', u'V106', u'L080', u'C230', u'P204',
        u'J063', u'J292', u'H102', u'T066', u'D243', u'H033', u'C094', u'M125', u'L402', u'G236', u'L323', u'N221',
        u'L184', u'M022', u'J043', u'L008', u'D328', u'E082', u'L305', u'G129', u'D168', u'D361', u'G139', u'K076',
        u'L046', u'K208', u'J344', u'N268', u'M352', u'L411', u'L162', u'S016', u'J149', u'L234', u'M139', u'N018',
        u'K306', u'L210', u'K273', u'J010', u'L149', u'M020', u'V075', u'P022', u'H291', u'J104', u'N159', u'G149',
        u'M403', u'H323', u'J067', u'J103', u'P092', u'L020', u'L127', u'H018', u'E267', u'K281', u'K198', u'K228',
        u'L051', u'T032', u'V006', u'H121', u'K196', u'P194', u'L089', u'M146', u'P090', u'K290', u'E199', u'C176',
        u'E021', u'L126', u'N267', u'N411', u'N425', u'S258', u'M230', u'P047', u'P244', u'M327', u'L072', u'E190',
        u'H052', u'N064', u'T097', u'S033', u'N347', u'L180', u'J313', u'H243', u'N421', u'E249', u'H014', u'H045',
        u'H307', u'N145', u'G043', u'H238', u'D292', u'P059', u'M359', u'P226', u'T067', u'L120', u'V299', u'H189',
        u'H141', u'K409', u'J347', u'N008', u'M037', u'H220', u'K124', u'G188', u'S213', u'T410', u'N123', u'N293',
        u'M053', u'N017', u'N187', u'J350', u'L047', u'J291', u'J233', u'K011', u'L200', u'P279', u'K135', u'P247',
        u'L022', u'L312', u'D297', u'L182', u'K081', u'K108', u'S196', u'S348', u'P332', u'P126', u'L300', u'E223',
        u'C025', u'K049', u'N125', u'G214', u'K255', u'M372', u'CB391', u'G012', u'M216', u'P329', u'E006', u'K206',
        u'L163', u'G285', u'T057', u'P193', u'M295', u'V030', u'S322', u'CB039', u'CB166', u'L224', u'H181', u'D306',
        u'J120', u'N058', u'M317', u'K119', u'T170', u'K336', u'K331', u'E208', u'E313', u'V190', u'J323', u'G273',
        u'D136', u'M288', u'H277', u'N041', u'K282', u'H030', u'M363', u'H230', u'T025', u'K412', u'K143', u'G081',
        u'CA367', u'D188', u'H039', u'CB188', u'E220', u'P012', u'P187', u'S034', u'J044', u'CB013', u'M225', u'K071',
        u'J229', u'S036', u'N117', u'T343', u'N244', u'L280', u'K051', u'M351', u'J065', u'G173', u'T034', u'D085',
        u'P360', u'N381', u'D208', u'N269', u'J258', u'T084', u'K312', u'T075', u'G147', u'M076', u'J048', u'M310',
        u'J202', u'G193', u'D132', u'K355', u'K012', u'P326', u'N197', u'P392', u'S249', u'L111', u'S207', u'E242',
        u'E111', u'K197', u'V062', u'E330', u'T275', u'M362', u'N009', u'P252', u'S008', u'S012', u'D371', u'G061',
        u'K365', u'J218', u'K310', u'H070', u'L223', u'S288', u'J209', u'J122', u'L123', u'N352', u'N049', u'M179',
        u'S115', u'N433', u'N343', u'H303', u'L125', u'L410', u'T255', u'K283', u'L116', u'P004', u'E188', u'D129',
        u'G069', u'CB388', u'K126', u'N056', u'N122', u'L015', u'N203', u'H177', u'N095', u'G167', u'H012', u'K090',
        u'K200', u'S333', u'L114', u'K219', u'CA391', u'H144', u'C206', u'K314', u'K204', u'L250', u'H173', u'L327',
        u'L328', u'D273', u'P023', u'P048', u'H264', u'M040', u'N442', u'N338', u'L066', u'L346', u'D315', u'H091',
        u'J009', u'N410', u'H073', u'H077', u'T169', u'N376', u'P218', u'S181', u'K322', u'S151', u'J222', u'P136',
        u'J334', u'H074', u'C031', u'L043', u'N367', u'P448', u'D042', u'T026', u'S009', u'N039', u'E329', u'M249',
        u'S433', u'T177', u'L279', u'H217', u'CB330', u'N329', u'N147', u'L316', u'N124', u'S088', u'L287', u'K298',
        u'P265', u'L245', u'T175', u'J050', u'C242', u'K152', u'J008', u'K131', u'K059', u'M325', u'L202', u'S116',
        u'P368', u'T049', u'S263', u'P386', u'J166', u'N406', u'P005', u'S164', u'E273', u'H134', u'G227', u'K166',
        u'G282', u'M198', u'E192', u'T206', u'N210', u'J139', u'V085', u'M143', u'G109', u'M106', u'L315', u'M014',
        u'M180', u'L417', u'G179', u'N034', u'H120', u'K053', u'H105', u'K161', u'M260', u'M219', u'M413', u'M006',
        u'H135', u'H224', u'G209', u'M187', u'G244', u'M254', u'M028', u'L421', u'S072', u'P250', u'J336', u'K038',
        u'S201', u'T294', u'J013', u'J317', u'N060', u'G241', u'E308', u'J286', u'E074', u'M138', u'M091', u'N059',
        u'M319', u'N319', u'J343', u'K106', u'N150', u'G259', u'H005', u'M172', u'M320', u'N152', u'E328', u'S095',
        u'E027', u'E229', u'K069', u'N285', u'P065', u'S107', u'K185', u'L176', u'M103', u'S132', u'K382', u'S265',
        u'D035', u'L148', u'E094', u'D195', u'P143', u'K122', u'G288', u'D109', u'N022', u'N230', u'G305', u'P322',
        u'K158', u'L321', u'C334', u'E233', u'M301', u'K113', u'N365', u'T102', u'K063', u'M052', u'L219', u'V104',
        u'H229', u'M001', u'P275', u'L256', u'N169', u'K254', u'G151', u'L011', u'H283', u'J316', u'G200', u'J197',
        u'J331', u'S020', u'G238', u'T386', u'N011', u'N377', u'L407', u'K263', u'G070', u'M059', u'N065', u'K061',
        u'H209', u'E114', u'H063', u'S443', u'S211', u'K236', u'P138', u'P328', u'J116', u'J287', u'V162', u'T106',
        u'P049', u'N044', u'N069', u'H236', u'H075', u'N020', u'M189', u'M313', u'N072', u'K008', u'J302', u'L115',
        u'M339', u'V175', u'P217', u'S220', u'S268', u'L168', u'K240', u'V196', u'D036', u'K195', u'K277', u'L299',
        u'T217', u'P263', u'K350', u'K052', u'J266', u'CB357', u'M110', u'S282', u'C056', u'G197', u'H157', u'H207',
        u'P346', u'J140', u'J259', u'L334', u'K286', u'K241', u'K243', u'K234', u'N195', u'K345', u'H022', u'N404',
        u'L164', u'L295', u'S374', u'S383', u'N208', u'N109', u'N351', u'L026', u'G008', u'K079', u'J241', u'J094',
        u'K018', u'D170', u'G087', u'L259', u'J076', u'E171', u'D185', u'J211', u'P284', u'M392', u'T153', u'J021',
        u'L307', u'L216', u'K227', u'M025', u'P087', u'H196', u'H194', u'J130', u'K142', u'S430', u'T135', u'E136',
        u'H123', u'H066', u'T434', u'T227', u'K364', u'T408', u'G203', u'D155', u'D246', u'G086', u'E146', u'C283',
        u'CB359', u'C348', u'CB404', u'T246', u'S229', u'J288', u'E253', u'G054', u'G318', u'D365', u'L152', u'L269',
        u'K098', u'N083', u'N131', u'M209', u'J185', u'K030', u'M114', u'J088', u'E227', u'L131', u'L239', u'S226',
        u'S005', u'P307', u'J219', u'N315', u'N204', u'T065', u'H298', u'G255', u'C231', u'K033', u'P045', u'L135',
        u'P125', u'M097', u'H165', u'P333', u'P108', u'P255', u'S274', u'P375', u'L354', u'K391', u'J249', u'P182',
        u'P327', u'M414', u'P043', u'M380', u'N173', u'N237', u'H275', u'G272', u'H098', u'D178', u'J235', u'M073',
        u'D242', u'C281', u'N121', u'G022', u'P313', u'T299', u'P251', u'N273', u'N357', u'P434', u'L257', u'J153',
        u'G174', u'L154', u'J349', u'K003', u'L288', u'K088', u'L044', u'N355', u'N181', u'H325', u'S159', u'J298',
        u'S105', u'N417', u'P377', u'S061', u'K402', u'L360', u'P076', u'M282', u'M369', u'P215', u'J110', u'L325',
        u'L050', u'P391', u'S118', u'S001', u'N258', u'P014', u'K127', u'M157', u'H028', u'K339', u'V103', u'T088',
        u'S248', u'P390', u'M208', u'D367', u'H200', u'K372', u'S112', u'T272', u'S223', u'N132', u'P290', u'J093',
        u'G108', u'G292', u'E002', u'K641', u'E201', u'K005', u'K642', u'J027', u'K144', u'J330', u'G184', u'C361',
        u'H003', u'P060', u'S045', u'S261', u'S163', u'N283', u'L017', u'J128', u'S158', u'L292', u'J121', u'J155',
        u'N614', u'L623', u'N612', u'N615', u'N613', u'N361', u'P129', u'P348', u'S321', u'L073', u'M011', u'N045',
        u'H027', u'E309', u'L389', u'N068', u'T428', u'S410', u'G268', u'C228', u'P447', u'K129', u'G042', u'E214',
        u'C310', u'CB090', u'M141', u'T366', u'J188', u'H131', u'K128', u'P104', u'E272', u'L319', u'L335', u'L090',
        u'M353', u'P427', u'C200', u'H310', u'J002', u'G322', u'L313', u'M132', u'S195', u'M418', u'K114', u'S082',
        u'H072', u'H110', u'V294', u'G113', u'H255', u'H161', u'S386', u'P248', u'L166', u'M092', u'G115', u'T008',
        u'M049', u'S013', u'S189', u'N178', u'N390', u'M416', u'N023', u'N077', u'M093', u'N289', u'N441', u'E331',
        u'P050', u'M257', u'L165', u'G290', u'H241', u'D018', u'J277', u'J201', u'M637', u'K638', u'M611', u'N278',
        u'G102', u'M088', u'M153', u'N341', u'N277', u'S372', u'L270', u'K259', u'J274', u'N062', u'E276', u'J054',
        u'D204', u'D398', u'M190', u'M147', u'S180', u'E325', u'H133', u'L351', u'H245', u'K625', u'J601', u'K626',
        u'K630', u'K633', u'K629', u'K631', u'K628', u'J030', u'H109', u'E241', u'M633', u'M630', u'M631', u'M629',
        u'M604', u'M632', u'H252', u'E078', u'D131', u'H059', u'P166', u'L284', u'G280', u'L109', u'E065', u'H326',
        u'H119', u'S111', u'T041', u'H190', u'H193', u'K608', u'V158', u'N232', u'H199', u'J318', u'K179', u'G038',
        u'V018', u'N242', u'S084', u'P617', u'P613', u'P612', u'P615', u'P616', u'H185', u'G171', u'K252', u'L233',
        u'L225', u'T303', u'S628', u'P606', u'S629', u'S630', u'S364', u'J208', u'N162', u'M051', u'S450', u'N444',
        u'P288', u'T147', u'S077', u'T180', u'N228', u'H287', u'E024', u'N225', u'P164', u'N006', u'G096', u'S017',
        u'M003', u'P335', u'M177', u'G303', u'E246', u'L601', u'L055', u'M130', u'S373', u'T270', u'M142', u'M289',
        u'S396', u'D349', u'D111', u'E018', u'CB394', u'D202', u'J156', u'J234', u'H148', u'E060', u'H174', u'M304',
        u'T007', u'T622', u'T613', u'T621', u'N618', u'N063', u'M276', u'T125', u'G155', u'N136', u'J631', u'H624',
        u'C155', u'K609', u'K610', u'G064', u'K614', u'K611', u'K613', u'K615', u'T247', u'E284', u'M419', u'L285',
        u'K269', u'L198', u'J108', u'J057', u'J091', u'N081', u'P077', u'M166', u'S267', u'S272', u'H011', u'J238',
        u'K639', u'E334', u'J629', u'G635', u'T264', u'S043', u'N205', u'L626', u'N625', u'N626', u'K636', u'N624',
        u'S345', u'M169', u'H237', u'G248', u'G199', u'P002', u'M368', u'N154', u'S416', u'S139', u'N607', u'N610',
        u'M612', u'M613', u'N608', u'N611', u'T215', u'E226', u'C134', u'K082', u'J223', u'H227', u'G142', u'L337',
        u'T122', u'J007', u'C084', u'T228', u'T602', u'L156', u'S361', u'J083', u'M270', u'A038', u'K217', u'M062',
        u'N308', u'K366', u'L170', u'M333', u'H068', u'N074', u'M337', u'J164', u'H001', u'G011', u'H308', u'J633',
        u'N256', u'N249', u'N332', u'T279', u'T165', u'S401', u'J309', u'M116', u'M140', u'H125', u'J060', u'L130',
        u'P413', u'L143', u'L388', u'K317', u'M196', u'P635', u'P633', u'N287', u'N617', u'N616', u'L621', u'N619',
        u'M620', u'N622', u'M624', u'N621', u'G222', u'G051', u'N114', u'S611', u'S612', u'S609', u'S610', u'S608',
        u'D029', u'N082', u'P276', u'L119', u'N395', u'S232', u'S168', u'S259', u'V614', u'V617', u'V616', u'V613',
        u'V615', u'V611', u'V612', u'P627', u'P626', u'P629', u'P144', u'M275', u'N373', u'L329', u'T043', u'S030',
        u'N334', u'J163', u'S178', u'P202', u'D101', u'N628', u'N627', u'N629', u'H155', u'T601', u'N214', u'L430',
        u'M018', u'L400', u'P406', u'V173', u'T606', u'T604', u'T605', u'N604', u'T607', u'P232', u'K010', u'T162',
        u'P624', u'S614', u'S618', u'S615', u'P620', u'S613', u'S616', u'P621', u'N032', u'P221', u'V632', u'V623',
        u'A617', u'A619', u'A618', u'A616', u'A621', u'A615', u'A614', u'C039', u'V208', u'M348', u'V603', u'V601',
        u'V602', u'V604', u'M203', u'M271', u'M277', u'J617', u'K620', u'K624', u'K623', u'K622', u'K618', u'K616',
        u'K619', u'K621', u'K617', u'N630', u'N631', u'K271', u'S625', u'S624', u'S120', u'S627', u'S626', u'J129',
        u'L303', u'T241', u'M186', u'M168', u'S064', u'E151', u'N363', u'H156', u'H111', u'K357', u'M082', u'T250',
        u'T244', u'M253', u'H329', u'J623', u'J622', u'J624', u'J627', u'K384', u'K343', u'L218', u'J159', u'P608',
        u'T612', u'T608', u'T610', u'T609', u'P162', u'L415', u'L362', u'P201', u'L331', u'J290', u'H213', u'L309',
        u'J119', u'H263', u'P393', u'N206', u'J299', u'M015', u'J053', u'V233', u'D303', u'L414', u'V098', u'M417',
        u'N321', u'P607', u'P609', u'P610', u'P611', u'G215', u'M621', u'M602', u'M623', u'M625', u'M622', u'M626',
        u'M628', u'CB293', u'D088', u'C346', u'H322', u'M640', u'M638', u'M639', u'K172', u'J016', u'M312', u'K229',
        u'P107', u'C327', u'C379', u'L052', u'M078', u'T001', u'K096', u'L612', u'L610', u'K640', u'L613', u'L609',
        u'L611', u'L608', u'K603', u'P206', u'M601', u'T229', u'J206', u'M603', u'M606', u'M605', u'P311', u'N418',
        u'H013', u'P602', u'S601', u'S602', u'L311', u'V352', u'P159', u'S042', u'P188', u'L314', u'J148', u'J115',
        u'P020', u'N368', u'M619', u'L614', u'M616', u'M617', u'M618', u'M615', u'M614', u'S620', u'S622', u'S621',
        u'S619', u'S623', u'T149', u'G242', u'V630', u'V629', u'H172', u'N108', u'P601', u'T318', u'M159', u'H228',
        u'N163', u'E282', u'T204', u'P245', u'J214', u'T143', u'P137', u'P312', u'T141', u'P036', u'D055', u'H254',
        u'T119', u'P394', u'T615', u'V625', u'V624', u'V620', u'V619', u'G082', u'A608', u'A609', u'A610', u'L617',
        u'L615', u'L616', u'T619', u'T611', u'V638', u'J025', u'N036', u'E115', u'T616', u'T620', u'T617', u'T618',
        u'M411', u'E210', u'P341', u'L633', u'L634', u'P619', u'P625', u'P622', u'P623', u'P618', u'T036', u'P403',
        u'P150', u'P235', u'P339', u'P186', u'T384', u'J607', u'K602', u'K606', u'K601', u'K607', u'K604', u'K605',
        u'CB335', u'L606', u'L604', u'L603', u'L602', u'L605', u'L607', u'P342', u'V605', u'V636', u'V635', u'N042',
        u'N280', u'E069', u'L629', u'L628', u'L625', u'L627', u'N606', u'P605', u'V178', u'A603', u'A620', u'A601',
        u'A602', u'A605', u'A606', u'A607', u'T603', u'T614', u'P630', u'P631', u'P632', u'S331', u'E141', u'M306',
        u'D100', u'L624', u'L619', u'L620', u'L618', u'L622', u'C240', u'M609', u'M608', u'M610', u'M607', u'M349',
        u'S210', u'N144', u'S606', u'S605', u'S604', u'S603', u'S607', u'J615', u'J628', u'H617', u'J630', u'M344',
        u'N199', u'K047', u'K022', u'S341', u'V610', u'V609', u'V607', u'V606', u'V608', u'H079', u'L039']

    horse_basic_info = test.download_horse_id_list(target_id_list)
    horse_basic_info.to_pickle('horse_info.p')
    horse_basic_info.to_excel('horse_info.xlsx')
