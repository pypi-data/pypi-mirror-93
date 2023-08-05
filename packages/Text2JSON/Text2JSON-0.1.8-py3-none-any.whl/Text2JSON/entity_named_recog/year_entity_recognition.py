import sys
from os.path import dirname, abspath
path = dirname(dirname(dirname(abspath(__file__))))
sys.path.append(path)
import re
import datetime
from datetime import date
from Text2JSON.entity_named_recog.entity_utils import *


def year_recon(line, placeholders_list: dict):
    line = year_relative_recognition(line, placeholders_list)
    line = year_absolute_recognition(line, placeholders_list)
    return line


def year_absolute_recognition(line, placeholders_list: dict):
    year_map = {'零': '0', '一': '1', '二': '2', '三': '3', '四': '4',
                '五': '5', '六': '6', '七': '7', '八': '8', '九': '9'}
    date_all = re.findall(r"(\d{4}年)", line)
    for data in date_all:
        index = line.index(data)
        first_line = line[0: index]
        sec_line = line[index + len(data):]

        # 确定年的开始时间和结束时间
        year = int(data.replace('年', ''))
        year_start = datetime.datetime(year, 1, 1)
        year_end = datetime.datetime(year, 12, 31)

        time_str = '“' + date_to_str(year_start) + "”" + "到" + '“' + date_to_str(year_end) + "”"
        placeholder = random_str()
        placeholders_list[placeholder] = (time_str, [year_start, year_end])
        line = first_line + placeholder + sec_line

    date_all = re.findall(r"(\d{2}年)", line)
    for data in date_all:
        index = line.index(data)
        first_line = line[0: index]
        sec_line = line[index + len(data):]

        year = int('20' + data.replace('年', ''))
        year_start = datetime.datetime(year, 1, 1)
        year_end = datetime.datetime(year, 12, 31)

        time_str = '“' + date_to_str(year_start) + "”" + "到" + '“' + date_to_str(year_end) + "”"
        placeholder = random_str()
        placeholders_list[placeholder] = (time_str, [year_start, year_end])
        line = first_line + placeholder + sec_line

    date_all = re.findall(r"([零一二三四五六七八九]{4}年)", line)
    for data in date_all:
        index = line.index(data)
        first_line = line[0: index]
        sec_line = line[index + len(data):]

        # 转成中文数字
        data = data.replace('年', '')
        year_str = ''
        for d_char in data:
            year_str += year_map[d_char]
        year = int(year_str)
        year_start = datetime.datetime(year, 1, 1)
        year_end = datetime.datetime(year, 12, 31)

        time_str = '“' + date_to_str(year_start) + "”" + "到" + '“' + date_to_str(year_end) + "”"
        placeholder = random_str()
        placeholders_list[placeholder] = (time_str, [year_start, year_end])
        line = first_line + placeholder + sec_line

    date_all = re.findall(r"([零一二三四五六七八九]{2}年)", line)
    for data in date_all:
        index = line.index(data)
        first_line = line[0: index]
        sec_line = line[index + len(data):]

        # 转成中文数字
        data = data.replace('年', '')
        year_str = ''
        for d_char in data:
            year_str += year_map[d_char]
        year = int('20' + year_str)
        year_start = datetime.datetime(year, 1, 1)
        year_end = datetime.datetime(year, 12, 31)

        time_str = '“' + date_to_str(year_start) + "”" + "到" + '“' + date_to_str(year_end) + "”"
        placeholder = random_str()
        placeholders_list[placeholder] = (time_str, [year_start, year_end])
        line = first_line + placeholder + sec_line

    return line


def year_relative_recognition(line, placeholders_list: dict):
    now_year = ['最近一年', '近一年', '最近1年', '近1年', '近年']
    cur_year = ['本年度', '本年', '今年', '这年']
    next_year = ['下1年', '下一年', '下年', '明年', '一年后']
    last_year = ['上1年', '上一年', '上年', '去年', '一年前']
    flag = True
    # 保证最长匹配优先, 因为存在共同后缀
    while flag:
        flag = False
        for year in now_year:
            if year in line:
                index = line.index(year)
                first_line = line[0: index]
                sec_line = line[index + len(year):]

                # now
                now = date.today()
                # 去年的同一时间
                try:
                    last_year_now = datetime.datetime(now.year - 1, now.month, now.day)
                except ValueError:
                    # 处理2月29日这种情况
                    last_year_now = datetime.datetime(now.year - 1, now.month, now.day - 1)

                # to str and insert into line
                time_str = '“' + date_to_str(last_year_now) + "”" + "到" + '“' + date_to_str(now) + "”"
                placeholder = random_str()
                placeholders_list[placeholder] = (time_str, [last_year_now, now])
                line = first_line + placeholder + sec_line
                flag = True
                break

    for year in cur_year:
        if year in line:
            index = line.index(year)
            first_line = line[0: index]
            sec_line = line[index + len(year):]

            # now
            now = date.today()
            # last year
            cur_year_start = datetime.datetime(now.year, 1, 1)
            cur_year_end = datetime.datetime(now.year, 12, 31)

            # to str and insert into line
            time_str = '“' + date_to_str(cur_year_start) + "”" + "到" + '“' + date_to_str(cur_year_end) + "”"
            placeholder = random_str()
            placeholders_list[placeholder] = (time_str, [cur_year_start, cur_year_end])
            line = first_line + placeholder + sec_line

    for year in next_year:
        if year in line:
            index = line.index(year)
            first_line = line[0: index]
            sec_line = line[index + len(year):]

            now = date.today()
            # 明年第一天喝最后一天
            next_year_start = datetime.datetime(now.year + 1, 1, 1)
            next_year_end = datetime.datetime(now.year + 1, 12, 31)

            # to str and insert into line
            time_str = '“' + date_to_str(next_year_start) + '”' + '到' + '“' + date_to_str(next_year_end) + '”'
            placeholder = random_str()
            placeholders_list[placeholder] = (time_str, [next_year_start, next_year_end])
            line = first_line + placeholder + sec_line

    for year in last_year:
        if year in line:
            index = line.index(year)
            first_line = line[0: index]
            sec_line = line[index + len(year):]

            now = date.today()
            # 明年第一天喝最后一天
            last_year_start = datetime.datetime(now.year - 1, 1, 1)
            last_year_end = datetime.datetime(now.year - 1, 12, 31)

            # to str and insert into line
            time_str = '“' + date_to_str(last_year_start) + '”' + '到' + '“' + date_to_str(last_year_end) + '”'
            placeholder = random_str()
            placeholders_list[placeholder] = (time_str, [last_year_start, last_year_end])
            line = first_line + placeholder + sec_line

    return line


def year_absolute_comfirm(line, placeholders_list: dict):
    # 需要找到最后出现的位置, '....2013年...' 不识别, '...2014年'识别
    # 重复出现,"2014年...,2014年"只识别最后一个
    year = None
    yaer_map = {'零': '0', '一': '1', '二': '2', '三': '3', '四': '4',
                '五': '5', '六': '6', '七': '7', '八': '8', '九': '9'}
    connect_char = ['-', '~', '到', '至']

    date_all = re.findall(r"(\d{4}年)", line)
    for data in date_all:
        index = line.rindex(data)
        if index + len(data) == len(line):
            year = int(data.replace('年', ''))
            line = line[:index]
            return line, year

    date_all = re.findall(r"(\d{2}年)", line)
    for data in date_all:
        index = line.rindex(data)
        if index + len(data) == len(line):
            year = int('20' + data.replace('年', ''))
            line = line[:index]
            return line, year

    date_all = re.findall(r"([零一二三四五六七八九]{4}年)", line)
    for data in date_all:
        index = line.rindex(data)
        if index + len(data) == len(line):
            # 转成中文数字
            data = data.replace('年', '')
            year_str = ''
            for d_char in data:
                year_str += yaer_map[d_char]
            year = int(year_str)
            line = line[:index]
            return line, year

    date_all = re.findall(r"([零一二三四五六七八九]{2}年)", line)
    for data in date_all:
        index = line.rindex(data)
        if index + len(data) == len(line):
            # 转成中文数字
            data = data.replace('年', '')
            year_str = ''
            for d_char in data:
                year_str += yaer_map[d_char]
            year = int('20' + year_str)
            line = line[:index]
            return line, year

    if len(line) >= 16 and line[-1] in connect_char:
        holder = line[-16:-1]
        if holder in placeholders_list.keys():
            _, time_list = placeholders_list[holder]
            if len(time_list) == 1 and time_list[0] is not None:
                return line[:-1] + '到', time_list[0].year

    return line, year


def year_relative_comfirm(line, placeholders_list: dict):
    # 只识别最后一个词
    cur_year = ['今年', '本年', '这年', '近年', '最近一年']
    next_year = ['下一年', '下年', '明年', '下1年']
    last_year = ['上一年', '上年', '去年', '上1年']
    year = None
    now = date.today()
    for data in cur_year:
        if data in line:
            index = line.rindex(data)
            if index + len(data) == len(line):
                year = now.year
                line = line[:index]
                return line, year
    for data in next_year:
        if data in line:
            index = line.rindex(data)
            if index + len(data) == len(line):
                year = now.year + 1
                line = line[:index]
                return line, year

    for data in last_year:
        if data in line:
            index = line.rindex(data)
            if index + len(data) == len(line):
                year = now.year - 1
                line = line[:index]
                return line, year
    return line, year
