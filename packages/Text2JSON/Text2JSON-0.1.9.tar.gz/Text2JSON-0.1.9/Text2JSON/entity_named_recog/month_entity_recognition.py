import sys
from os.path import dirname, abspath
path = dirname(dirname(dirname(abspath(__file__))))
sys.path.append(path)
import datetime
import re
from datetime import date, timedelta
import calendar
from Text2JSON.entity_named_recog.entity_utils import *
from Text2JSON.entity_named_recog.year_entity_recognition import year_absolute_comfirm, year_relative_comfirm


def month_recon(line, placeholders_list: dict):
    line = month_relative_recognition(line, placeholders_list)
    line = month_absolute_recognition(line, placeholders_list)
    return line


# 月相对位置识别
def month_relative_recognition(line, placeholders_list: dict):
    cur_month = ['今个月', '这个月', '本月', '今月', '这月']
    now_month = ['最近一个月', '近一个月', '最近1个月', '近1个月', '近月']
    next_month = ['下1个月', '下一个月', '下一月', '下个月', '下月', '一个月后', '1个月后']
    last_month = ['上1个月', '上一个月', '上一月', '上个月', '上月', '一个月前', '1个月前']
    flag = True
    for month in cur_month:
        if month in line:
            index = line.index(month)
            first_line = line[0: index]
            sec_line = line[index + len(month):]

            # now
            now = date.today()

            # 本月第一天喝最后一天
            this_month_start = datetime.datetime(now.year, now.month, 1)
            this_month_end = datetime.datetime(now.year, now.month, calendar.monthrange(now.year, now.month)[1])

            # to str and insert into line
            time_str = '“' + date_to_str(this_month_start) + "”" + "到" + '“' + date_to_str(this_month_end) + "”"
            placeholder = random_str()
            placeholders_list[placeholder] = (time_str, [this_month_start, this_month_end])
            line = first_line + placeholder + sec_line

    # 保证最长匹配优先
    while flag:
        flag = False
        for month in now_month:
            if month in line:
                index = line.index(month)
                first_line = line[0: index]
                sec_line = line[index + len(month):]

                # now
                now = date.today()
                # 本月的第一天
                now_month_start = datetime.datetime(now.year, now.month, 1)
                # 上月的最后一天
                last_month_end = now_month_start + timedelta(days=-1)
                cnt = 0
                before_n_days = None
                while True:
                    try:
                        before_n_days = datetime.datetime(last_month_end.year, last_month_end.month, now.day - cnt)
                        break
                    except ValueError:
                        cnt += 1
                        continue
                assert before_n_days is not None, '逻辑错误'
                # to str and insert into line
                time_str = '“' + date_to_str(before_n_days) + "”" + "到" + '“' + date_to_str(now) + "”"
                placeholder = random_str()
                placeholders_list[placeholder] = (time_str, [before_n_days, now])
                line = first_line + placeholder + sec_line
                flag = True
                break

    for month in next_month:
        if month in line:
            index = line.index(month)
            first_line = line[0: index]
            sec_line = line[index + len(month):]

            now = date.today()
            # 本月最后一天
            this_month_end = datetime.datetime(now.year, now.month, calendar.monthrange(now.year, now.month)[1])

            # 下一月第一天和最后一天
            next_month_start = this_month_end + timedelta(days=1)
            next_month_end = datetime.datetime(next_month_start.year, next_month_start.month,
                                               calendar.monthrange(next_month_start.year,
                                                                   next_month_start.month)[1])
            # to str and insert into line
            time_str = '“' + date_to_str(next_month_start) + '”' + '到' + '“' + date_to_str(next_month_end) + '”'
            placeholder = random_str()
            placeholders_list[placeholder] = (time_str, [next_month_start, next_month_end])
            line = first_line + placeholder + sec_line

    for month in last_month:
        if month in line:
            index = line.index(month)
            first_line = line[0: index]
            sec_line = line[index + len(month):]

            now = date.today()
            # 当前月第一天
            this_month_start = datetime.datetime(now.year, now.month, 1)
            # 上月最后一天和上个月第一天
            last_month_end = this_month_start - timedelta(days=1)
            last_month_start = datetime.datetime(last_month_end.year, last_month_end.month, 1)

            # to str and insert into line
            time_str = '“' + date_to_str(last_month_start) + '”' + '到' + '“' + date_to_str(last_month_end) + '”'
            placeholder = random_str()
            placeholders_list[placeholder] = (time_str, [last_month_start, last_month_end])
            line = first_line + placeholder + sec_line

    return line


# 月相对位置识别
def month_absolute_recognition(line, placeholders_list: dict):
    now = date.today()
    month_map = {'一': '1', '二': '2', '三': '3', '四': '4',
                 '五': '5', '六': '6', '七': '7', '八': '8', '九': '9'}
    # 数字 月份 10,11,12
    date_all = re.findall(r"(\d{1,2}月[份]?)", line)
    for data in date_all:
        index = line.index(data)
        first_line = line[0: index]
        sec_line = line[index + len(data):]
        month = int(re.sub(r'(月[份]?)', '', data))

        handle_line, year = year_absolute_comfirm(first_line, placeholders_list)
        if year is None:
            handle_line, year = year_relative_comfirm(first_line, placeholders_list)
        year = now.year if year is None else year

        try:
            month_start = datetime.datetime(year, month, 1)
            month_end = datetime.datetime(year, month,
                                          calendar.monthrange(year, month)[1])
        except ValueError:
            # 识别不出来就认为是错误，后续不再识别
            time_str = data
            placeholder = random_str()
            placeholders_list[placeholder] = (time_str, [None, None])
            line = first_line + placeholder + sec_line
            continue
        # 用占位符暂时代替，否则就会无限重复
        time_str = '“' + date_to_str(month_start) + "”" + "到" + '“' + date_to_str(month_end) + "”"
        placeholder = random_str()
        placeholders_list[placeholder] = (time_str, [month_start, month_end])
        line = handle_line + placeholder + sec_line

    date_all = re.findall(r"([第]?十[一二]?[个]?月[份]?)", line)
    for data in date_all:
        index = line.index(data)
        first_line = line[0: index]
        sec_line = line[index + len(data):]
        month = re.sub(r'([个]?月[份]?)', '', data)
        month = re.sub(r'([第])', '', month)

        if len(month) == 1:
            month = 10
        else:
            month = 10 + int(month_map[re.sub(r'(十)', '', data)])

        handle_line, year = year_absolute_comfirm(first_line, placeholders_list)
        if year is None:
            handle_line, year = year_relative_comfirm(first_line, placeholders_list)
        year = now.year if year is None else year

        try:
            month_start = datetime.datetime(year, month, 1)
            month_end = datetime.datetime(year, month,
                                          calendar.monthrange(year, month)[1])
        except ValueError:
            # 识别不出来就认为是错误，后续不再识别
            time_str = data
            placeholder = random_str()
            placeholders_list[placeholder] = (time_str, [None, None])
            line = first_line + placeholder + sec_line
            continue
        # 用占位符暂时代替，否则就会无限重复
        time_str = '“' + date_to_str(month_start) + "”" + "到" + '“' + date_to_str(month_end) + "”"
        placeholder = random_str()
        placeholders_list[placeholder] = (time_str, [month_start, month_end])
        line = handle_line + placeholder + sec_line

    date_all = re.findall(r"([第]?[一二三四五六七八九][个]?月[份]?)", line)
    for data in date_all:
        index = line.index(data)
        first_line = line[0: index]
        sec_line = line[index + len(data):]
        month = re.sub(r'([个]?月[份]?)', '', data)
        month = re.sub(r'([第])', '', month)
        month = int(month_map[month])
        handle_line, year = year_absolute_comfirm(first_line, placeholders_list)
        if year is None:
            handle_line, year = year_relative_comfirm(first_line, placeholders_list)
        year = now.year if year is None else year

        try:
            month_start = datetime.datetime(year, month, 1)
            month_end = datetime.datetime(year, month,
                                          calendar.monthrange(year, month)[1])
        except ValueError:
            # 识别不出来就认为是错误，后续不再识别
            time_str = data
            placeholder = random_str()
            placeholders_list[placeholder] = (time_str, [None, None])
            line = first_line + placeholder + sec_line
            continue
        # 用占位符暂时代替，否则就会无限重复
        time_str = '“' + date_to_str(month_start) + "”" + "到" + '“' + date_to_str(month_end) + "”"
        placeholder = random_str()
        placeholders_list[placeholder] = (time_str, [month_start, month_end])
        line = handle_line + placeholder + sec_line

    date_all = re.findall(r"(最后[一1][个]?月[份]?)", line)
    for data in date_all:
        index = line.index(data)
        first_line = line[0: index]
        sec_line = line[index + len(data):]

        month = 12
        handle_line, year = year_absolute_comfirm(first_line, placeholders_list)
        if year is None:
            handle_line, year = year_relative_comfirm(first_line, placeholders_list)
        year = now.year if year is None else year

        try:
            month_start = datetime.datetime(year, month, 1)
            month_end = datetime.datetime(year, month,
                                          calendar.monthrange(year, month)[1])
        except ValueError:
            # 识别不出来就认为是错误，后续不再识别
            time_str = data
            placeholder = random_str()
            placeholders_list[placeholder] = (time_str, [None, None])
            line = first_line + placeholder + sec_line
            continue
        # 用占位符暂时代替，否则就会无限重复
        time_str = '“' + date_to_str(month_start) + "”" + "到" + '“' + date_to_str(month_end) + "”"
        placeholder = random_str()
        placeholders_list[placeholder] = (time_str, [month_start, month_end])
        line = handle_line + placeholder + sec_line
    return line


def month_absolute_comfirm(line, placeholders_list: dict):
    # 需要找到最后出现的位置, '....2013年...' 不识别, '...2014年'识别
    # 重复出现,"2014年...,2014年"只识别最后一个
    month = None
    year = None
    now = date.today()
    month_map = {'一': '1', '二': '2', '三': '3', '四': '4',
                 '五': '5', '六': '6', '七': '7', '八': '8', '九': '9'}
    connect_char = ['-', '~', '到', '至']

    date_all = re.findall(r"(\d{1,2}月[份]?)", line)
    for data in date_all:
        index = line.rindex(data)
        if index + len(data) == len(line):
            month = int(data.replace('月', ''))
            line = line[:index]

            line, year = year_absolute_comfirm(line, placeholders_list)
            if year is None:
                line, year = year_relative_comfirm(line, placeholders_list)
            year = now.year if year is None else year
            return line, year, month

    # 处理10月,11月,12月
    date_all = re.findall(r'([十][一二]?月[份]?)', line)
    for data in date_all:
        index = line.rindex(data)
        if index + len(data) == len(line):
            line = line[:index]
            # 转成中文数字
            data = data.replace('月', '')
            data = data.replace('十', '')
            month_str = '0'
            for d_char in data:
                month_str += month_map[d_char]
            month = 10 + int(month_str)
            line, year = year_absolute_comfirm(line, placeholders_list)
            if year is None:
                line, year = year_relative_comfirm(line, placeholders_list)
            year = now.year if year is None else year
            return line, year, month

    # 处理1-9月
    date_all = re.findall(r"([一二三四五六七八九]月[份]?)", line)
    for data in date_all:
        index = line.rindex(data)
        if index + len(data) == len(line):
            # 转成中文数字
            data = data.replace('月', '')
            month_str = ''
            for d_char in data:
                month_str += month_map[d_char]
            month = int(month_str)
            line = line[:index]
            line, year = year_absolute_comfirm(line, placeholders_list)
            if year is None:
                line, year = year_relative_comfirm(line, placeholders_list)
            year = now.year if year is None else year
            return line, year, month

    if len(line) >= 16 and line[-1] in connect_char:
        holder = line[-16:-1]
        if holder in placeholders_list.keys():
            _, time_list = placeholders_list[holder]
            if len(time_list) == 1 and time_list[0] is not None:
                return line[:-1] + '到', time_list[0].year, time_list[0].month

    return line, year, month


# 月相对位置确认
def month_relative_comfirm(line, placeholders_list: dict):
    # 只识别最后一个词
    cur_month = ['今月', '本月', '这个月', '这月']
    next_month = ['下1个月', '下一个月', '下一月', '下个月', '下月', '一个月后', '1个月后']
    last_month = ['上1个月', '上一个月', '上一月', '上个月', '上月', '一个月前', '1个月前']
    year = None
    month = None
    # 需要把年加进来
    now = date.today()
    for data in cur_month:
        if data in line:
            index = line.rindex(data)
            if index + len(data) == len(line):
                year = now.year
                month = now.month
                line = line[:index]
                return line, year, month
    for data in next_month:
        if data in line:
            index = line.rindex(data)
            if index + len(data) == len(line):
                month_end = datetime.datetime(now.year, now.month, calendar.monthrange(now.year, now.month)[1])
                next_month_start = month_end + timedelta(days=1)
                year = next_month_start.year
                month = next_month_start.month
                line = line[:index]
                return line, year, month

    for data in last_month:
        if data in line:
            index = line.rindex(data)
            if index + len(data) == len(line):
                month_start = datetime.datetime(now.year, now.month, 1)
                last_month_end = month_start - timedelta(days=1)
                year = last_month_end.year
                month = last_month_end.month
                line = line[:index]
                return line, year, month
    return line, year, month


if __name__ == '__main__':
    ''
    # placeholders = {}
    # example1 = '明年11月, 今年12月'
    # sentence = month_recon(example1, placeholders)
    # for holder, data in placeholders.items():
    #     sentence = sentence.replace(holder, data[0])
    # print(example1)
    # print('10', sentence)
    # example1 = '最近一个月， 最近一个月'
    # placeholders_list = []
    # sentence, placeholders = month_absolute_recon(example1)
    # placeholders_list.extend(placeholders)
    # sentence, placeholders = month_relative_recon(sentence)
    # placeholders_list.extend(placeholders)
    # for token, holder in placeholders_list:
    #     sentence = sentence.replace(holder, token)
    # print(sentence)
    #
    # example2 = '去年2月，今年6月份，下年7月，16年6月，2017年十二月，16年二月, 一六年十一月，二零零零年十二月'
    # placeholders_list = []
    # sentence, placeholders = month_absolute_recon(example2)
    # placeholders_list.extend(placeholders)
    # sentence, placeholders = month_relative_recon(sentence)
    # placeholders_list.extend(placeholders)
    # for token, holder in placeholders_list:
    #     sentence = sentence.replace(holder, token)
    # print(sentence)
    #
    # example3 = 'sss12月, 去年12月'
    # example4 = 'sss十二月, 今年二月'
    # sentence, year, month = month_absolute_comfirm(example3)
    # print(sentence, year, month)
    # sentence, year, month = month_absolute_comfirm(example4)
    # print(sentence, year, month)
    # example4 = 'sss十二月, 明年四月'
    # sentence, year, month = month_absolute_comfirm(example4)
    # print(sentence, year, month)
    # example4 = 'sss十二月, 19年四月'
    # sentence, year, month = month_absolute_comfirm(example4)
    # print(sentence, year, month)
    # example4 = 'sss十二月, 零零年四月'
    # sentence, year, month = month_absolute_comfirm(example4)
    # print(sentence, year, month)
    #
    # example5 = 'sss下一个月'
    # sentence, year, month = month_relative_comfirm(example5)
    # print(sentence, year, month)
    #
    # example5 = 'sss上一个月'
    # sentence, year, month = month_relative_comfirm(example5)
    # print(sentence, year, month)
