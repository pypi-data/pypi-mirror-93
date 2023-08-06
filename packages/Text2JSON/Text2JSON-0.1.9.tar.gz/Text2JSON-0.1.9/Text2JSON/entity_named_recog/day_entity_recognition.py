import sys
from os.path import dirname, abspath
path = dirname(dirname(dirname(abspath(__file__))))
sys.path.append(path)
import datetime
import re
from datetime import date, timedelta
from Text2JSON.entity_named_recog.month_entity_recognition import month_absolute_comfirm, month_relative_comfirm
from Text2JSON.entity_named_recog.entity_utils import *


def day_recon(line, placeholders_list: dict):
    line = day_relative_recognition(line, placeholders_list)
    line = day_absolute_recognition(line, placeholders_list)
    return line


def day_absolute_recognition(line, placeholders_list: dict):
    # 需要找到最后出现的位置, '....2013年...' 不识别, '...2014年'识别
    # 重复出现,"2014年...,2014年"只识别最后一个
    now = date.today()
    day_map = {'一': '1', '二': '2', '三': '3', '四': '4',
               '五': '5', '六': '6', '七': '7', '八': '8', '九': '9'}

    # 出日01-31日
    date_all = re.findall(r"(\d{1,2}日)", line)
    for data in date_all:
        index = line.index(data)
        first_line = line[0: index]
        sec_line = line[index + len(data):]

        day = int(data.replace('日', ''))

        # 确定年月
        handle_line, year, month = month_relative_comfirm(first_line, placeholders_list)
        if year is None:
            handle_line, year, month = month_absolute_comfirm(first_line, placeholders_list)
        year = now.year if year is None else year
        month = now.month if month is None else month
        try:
            # 解析不出来的日期需要跳过
            target_day = datetime.datetime(year, month, day)
        except ValueError:
            # 识别不出来就认为是错误，后续不再识别
            time_str = data
            placeholder = random_str()
            placeholders_list[placeholder] = (time_str, [None])
            line = first_line + placeholder + sec_line
            continue
        assert target_day is not None, '逻辑错误'
        time_str = '“' + date_to_str(target_day) + "”"
        placeholder = random_str()
        placeholders_list[placeholder] = (time_str, [target_day])
        line = handle_line + placeholder + sec_line

    # 处理 十 ~ 三十一 中文日期
    date_all = re.findall(r'([二三]?[十][一二三四五六七八九]?日)', line)
    for data in date_all:
        index = line.index(data)
        first_line = line[0: index]
        sec_line = line[index + len(data):]

        # 确定年月
        handle_line, year, month = month_relative_comfirm(first_line, placeholders_list)
        if year is None:
            handle_line, year, month = month_absolute_comfirm(first_line, placeholders_list)
        year = now.year if year is None else year
        month = now.month if month is None else month

        # 转成数字
        data_digit = data.replace('日', '')
        prefix = data_digit[0:data_digit.index('十')]
        postfix = data_digit[data_digit.index('十') + 1:]
        # 10
        if len(prefix) == 0 and len(postfix) == 0:
            day = 10
        # 11 ~ 19
        elif len(prefix) == 0 and len(postfix) != 0:
            day = 10 + int(day_map[postfix])
        # 20, 30
        elif len(prefix) != 0 and len(postfix) == 0:
            day = int(day_map[prefix]) * 10
        else:
            # 21 ~ 29
            day = int(day_map[prefix]) * 10 + int(day_map[postfix])
        try:
            # 解析不出来的日期需要跳过
            target_day = datetime.datetime(year, month, day)
        except ValueError:
            # 识别不出来就认为是错误，后续不再识别
            time_str = data
            placeholder = random_str()
            placeholders_list[placeholder] = (time_str, [None])
            line = first_line + placeholder + sec_line
            continue
        assert target_day is not None, '逻辑错误'
        time_str = '“' + date_to_str(target_day) + "”"
        placeholder = random_str()
        placeholders_list[placeholder] = (time_str, [target_day])
        line = handle_line + placeholder + sec_line

    # 处理 一 ~ 九 中文日期
    date_all = re.findall(r'([一二三四五六七八九]日)', line)
    for data in date_all:
        index = line.index(data)
        first_line = line[0: index]
        sec_line = line[index + len(data):]

        # 确定年月
        handle_line, year, month = month_relative_comfirm(first_line, placeholders_list)
        if year is None:
            handle_line, year, month = month_absolute_comfirm(first_line, placeholders_list)
        year = now.year if year is None else year
        month = now.month if month is None else month

        # 转成数字
        day = int(day_map[data.replace('日', '')])

        try:
            # 解析不出来的日期需要跳过
            target_day = datetime.datetime(year, month, day)
        except ValueError:
            # 识别不出来就认为是错误，后续不再识别
            time_str = data
            placeholder = random_str()
            placeholders_list[placeholder] = (time_str, [None])
            line = first_line + placeholder + sec_line
            continue
        assert target_day is not None, '逻辑错误'
        time_str = '“' + date_to_str(target_day) + "”"
        placeholder = random_str()
        placeholders_list[placeholder] = (time_str, [target_day])
        line = handle_line + placeholder + sec_line

    return line


def day_relative_recognition(line, placeholders_list: dict):
    cur_day = ['今天', '这天']
    next_day = ['明天', '下一天', '一天后', '后一天']
    last_day = ['昨天', '上一天', '一天前', '前一天']
    day_map = {'一': '1', '二': '2', '三': '3', '四': '4',
               '五': '5', '六': '6', '七': '7', '八': '8', '九': '9', '两': '2', '十': '10'}
    for day in cur_day:
        if day in line:
            index = line.index(day)
            first_line = line[0: index]
            sec_line = line[index + len(day):]

            # now
            now = date.today()

            time_str = '“' + date_to_str(now) + "”"
            placeholder = random_str()
            placeholders_list[placeholder] = (time_str, [now])
            line = first_line + placeholder + sec_line

    for day in next_day:
        if day in line:
            index = line.index(day)
            first_line = line[0: index]
            sec_line = line[index + len(day):]

            # now
            now = date.today()

            next_day_date = now + timedelta(days=1)

            # to str and insert into line
            time_str = '“' + date_to_str(next_day_date) + "”"
            placeholder = random_str()
            placeholders_list[placeholder] = (time_str, [next_day_date])
            line = first_line + placeholder + sec_line

    for day in last_day:
        if day in line:
            index = line.index(day)
            first_line = line[0: index]
            sec_line = line[index + len(day):]

            now = date.today()
            # 前一天
            next_n_date = now + timedelta(days=-1)

            # to str and insert into line
            time_str = '“' + date_to_str(next_n_date) + '”'
            placeholder = random_str()
            placeholders_list[placeholder] = (time_str, [next_n_date])
            line = first_line + placeholder + sec_line

    date_all = re.findall(r'(\d{1,2}[日天]后)', line)
    for data in date_all:
        index = line.index(data)
        first_line = line[0: index]
        sec_line = line[index + len(data):]

        day_delta = int(re.sub(r'[日天]后', '', data))
        now = date.today()
        # 前一天
        next_n_date = now + timedelta(days=int(day_delta))

        # to str and insert into line
        time_str = '“' + date_to_str(next_n_date) + '”'
        placeholder = random_str()
        placeholders_list[placeholder] = (time_str, [next_n_date])
        line = first_line + placeholder + sec_line

    date_all = re.findall(r'([二三四五六七八九]?[十]?[一两二三四五六七八九十][日天]后)', line)
    for data in date_all:
        index = line.index(data)
        first_line = line[0: index]
        sec_line = line[index + len(data):]

        day_delta = re.sub(r'[日天]后', '', data)
        now = date.today()

        try:
            # 解析分钟
            if len(day_delta) > 1:
                if '十' not in day_delta:
                    # 错误处理
                    raise ValueError
                else:
                    pre_day = day_delta[0:day_delta.index('十')]
                    post_minute = day_delta[day_delta.index('十') + 1:]
                    # 10
                    if len(pre_day) == 0 and len(post_minute) == 0:
                        day = 10
                    # 11 ~ 19
                    elif len(pre_day) == 0 and len(post_minute) != 0:
                        day = 10 + int(day_map[post_minute])
                    # 20, 30
                    elif len(pre_day) != 0 and len(post_minute) == 0:
                        day = int(day_map[pre_day]) * 10
                    else:
                        # 21 ~ 24
                        day = int(day_map[pre_day]) * 10 + int(day_map[post_minute])
            else:
                day = int(day_map[day_delta])
        except ValueError:
            # 识别不出来就认为是错误，后续不再识别
            time_str = data
            placeholder = random_str()
            placeholders_list[placeholder] = (time_str, [None])
            line = first_line + placeholder + sec_line
            continue
        # 前一天
        next_n_date = now + timedelta(days=day)

        # to str and insert into line
        time_str = '“' + date_to_str(next_n_date) + '”'
        placeholder = random_str()
        placeholders_list[placeholder] = (time_str, [next_n_date])
        line = first_line + placeholder + sec_line

    date_all = re.findall(r'(\d{1,2}[日天]前)', line)
    for data in date_all:
        index = line.index(data)
        first_line = line[0: index]
        sec_line = line[index + len(data):]

        day_delta = int(re.sub(r'[日天]前', '', data))
        now = date.today()
        # 前一天
        last_n_date = now - timedelta(days=int(day_delta))

        # to str and insert into line
        time_str = '“' + date_to_str(last_n_date) + '”'
        placeholder = random_str()
        placeholders_list[placeholder] = (time_str, [last_n_date])
        line = first_line + placeholder + sec_line

    date_all = re.findall(r'([二三四五六七八九]?[十]?[一两二三四五六七八九十][日天]前)', line)
    for data in date_all:
        index = line.index(data)
        first_line = line[0: index]
        sec_line = line[index + len(data):]

        day_delta = re.sub(r'[日天]前', '', data)
        now = date.today()

        try:
            # 解析分钟
            if len(day_delta) > 1:
                if '十' not in day_delta:
                    # 错误处理
                    raise ValueError
                else:
                    pre_day = day_delta[0:day_delta.index('十')]
                    post_minute = day_delta[day_delta.index('十') + 1:]
                    # 10
                    if len(pre_day) == 0 and len(post_minute) == 0:
                        day = 10
                    # 11 ~ 19
                    elif len(pre_day) == 0 and len(post_minute) != 0:
                        day = 10 + int(day_map[post_minute])
                    # 20, 30
                    elif len(pre_day) != 0 and len(post_minute) == 0:
                        day = int(day_map[pre_day]) * 10
                    else:
                        # 21 ~ 24
                        day = int(day_map[pre_day]) * 10 + int(day_map[post_minute])
            else:
                day = int(day_map[day_delta])
        except ValueError:
            # 识别不出来就认为是错误，后续不再识别
            time_str = data
            placeholder = random_str()
            placeholders_list[placeholder] = (time_str, [None])
            line = first_line + placeholder + sec_line
            continue

        last_n_date = now - timedelta(days=day)
        # to str and insert into line
        time_str = '“' + date_to_str(last_n_date) + '”'
        placeholder = random_str()
        placeholders_list[placeholder] = (time_str, [last_n_date])
        line = first_line + placeholder + sec_line
    return line


def day_relative_comfirm(line, placeholders_list: dict):
    cur_day = ['今天', '这天', '今']
    next_day = ['明天', '下一天', '一天后', '后一天', '下1天', '1天后', '后1天', '明']
    last_day = ['昨天', '上一天', '一天前', '前一天', '上一天', '一天前', '前一天']
    day_map = {'一': '1', '二': '2', '三': '3', '四': '4',
               '五': '5', '六': '6', '七': '7', '八': '8', '九': '9', '两': '2'}
    # 连字符 = []
    now = date.today()
    for data in cur_day:
        if data in line:
            index = line.rindex(data)
            if index + len(data) == len(line):
                line = line[:index]
                return line, now.year, now.month, now.day

    for data in next_day:
        if data in line:
            index = line.rindex(data)
            if index + len(data) == len(line):
                line = line[:index]
                next_day_date = now + timedelta(days=1)
                return line, next_day_date.year, next_day_date.month, next_day_date.day

    for data in last_day:
        if data in line:
            index = line.rindex(data)
            if index + len(data) == len(line):
                line = line[:index]
                last_day_date = now - timedelta(days=1)
                return line, last_day_date.year, last_day_date.month, last_day_date.day

    date_all = re.findall(r'(\d{1,2}[日天]后)', line)
    for data in date_all:
        index = line.rindex(data)
        if index + len(data) == len(line):
            line = line[:index]
            day_delta = int(re.sub(r'[日天]后', '', data))
            now = date.today()
            next_n_date = now + timedelta(days=int(day_delta))
            return line, next_n_date.year, next_n_date.month, next_n_date.day

    date_all = re.findall(r'([二三四五六七八九]十[一二三四五六七八九]?[日天]后)', line)
    for data in date_all:
        index = line.rindex(data)
        if index + len(data) == len(line):
            line = line[:index]

            day_delta = re.sub(r'[日天]后', '', data)
            now = date.today()

            prefix = day_delta[0:day_delta.index('十')]
            postfix = day_delta[day_delta.index('十') + 1:]
            # 10
            if len(prefix) == 0 and len(postfix) == 0:
                day = 10
            # 11 ~ 19
            elif len(prefix) == 0 and len(postfix) != 0:
                day = 10 + int(day_map[postfix])
            # 20, 30
            elif len(prefix) != 0 and len(postfix) == 0:
                day = int(day_map[prefix]) * 10
            else:
                # 21 ~ 29
                day = int(day_map[prefix]) * 10 + int(day_map[postfix])

            # 前一天
            next_n_date = now + timedelta(days=day)
            return line, next_n_date.year, next_n_date.month, next_n_date.day

    date_all = re.findall(r'([两一二三四五六七八九][日天]后)', line)
    for data in date_all:
        index = line.rindex(data)
        if index + len(data) == len(line):
            line = line[:index]
            day_delta = re.sub(r'[日天]后', '', data)
            now = date.today()
            next_n_date = now + timedelta(days=int(day_map[day_delta]))
            return line, next_n_date.year, next_n_date.month, next_n_date.day

    date_all = re.findall(r'(\d{1,2}[日天]前)', line)
    for data in date_all:
        index = line.rindex(data)
        if index + len(data) == len(line):
            line = line[:index]

            day_delta = int(re.sub(r'[日天]前', '', data))
            now = date.today()
            # 前一天
            last_n_date = now - timedelta(days=int(day_delta))
            return line, last_n_date.year, last_n_date.month, last_n_date.day

    date_all = re.findall(r'([二三四五六七八九]十[一二三四五六七八九]?[日天]前)', line)
    for data in date_all:
        index = line.rindex(data)
        if index + len(data) == len(line):
            line = line[:index]

            day_delta = re.sub(r'[日天]前', '', data)
            now = date.today()

            prefix = day_delta[0:day_delta.index('十')]
            postfix = day_delta[day_delta.index('十') + 1:]
            # 10
            if len(prefix) == 0 and len(postfix) == 0:
                day = 10
            # 11 ~ 19
            elif len(prefix) == 0 and len(postfix) != 0:
                day = 10 + int(day_map[postfix])
            # 20, 30
            elif len(prefix) != 0 and len(postfix) == 0:
                day = int(day_map[prefix]) * 10
            else:
                # 21 ~ 29
                day = int(day_map[prefix]) * 10 + int(day_map[postfix])

            # 前一天
            next_n_date = now - timedelta(days=day)
            return line, next_n_date.year, next_n_date.month, next_n_date.day

    date_all = re.findall(r'([两一二三四五六七八九][日天]前)', line)
    for data in date_all:
        index = line.rindex(data)
        if index + len(data) == len(line):
            line = line[:index]

            day_delta = re.sub(r'[日天]前', '', data)
            now = date.today()

            last_n_date = now - timedelta(days=int(day_map[day_delta]))
            return line, last_n_date.year, last_n_date.month, last_n_date.day

    return line, None, None, None


def day_absolute_comfirm(line, placeholders_list: dict):
    now = date.today()
    day_map = {'一': '1', '二': '2', '三': '3', '四': '4',
               '五': '5', '六': '6', '七': '7', '八': '8', '九': '9'}
    connect_char = ['-', '~', '到', '至']
    # 出日01-31日
    date_all = re.findall(r"(\d{1,2}日)", line)
    for data in date_all:
        index = line.rindex(data)
        if index + len(data) == len(line):
            line = line[:index]

            # 确定年月日
            day = int(data.replace('日', ''))
            line, year, month = month_relative_comfirm(line, placeholders_list)
            if year is None:
                line, year, month = month_absolute_comfirm(line, placeholders_list)
            year = now.year if year is None else year
            month = now.month if month is None else month
            return line, year, month, day

    # 处理 十 ~ 三十一 中文日期
    date_all = re.findall(r'([二三]?[十][一二三四五六七八九]?日)', line)
    for data in date_all:
        index = line.rindex(data)
        if index + len(data) == len(line):
            line = line[:index]

            # 确定年月
            line, year, month = month_relative_comfirm(line, placeholders_list)
            if year is None:
                line, year, month = month_absolute_comfirm(line, placeholders_list)
            year = now.year if year is None else year
            month = now.month if month is None else month

            # 转成数字
            data_digit = data.replace('日', '')
            prefix = data_digit[0:data_digit.index('十')]
            postfix = data_digit[data_digit.index('十') + 1:]
            # 10
            if len(prefix) == 0 and len(postfix) == 0:
                day = 10
            # 11 ~ 19
            elif len(prefix) == 0 and len(postfix) != 0:
                day = 10 + int(day_map[postfix])
            # 20, 30
            elif len(prefix) != 0 and len(postfix) == 0:
                day = int(day_map[prefix]) * 10
            else:
                # 21 ~ 29
                day = int(day_map[prefix]) * 10 + int(day_map[postfix])
            return line, year, month, day

    # 处理 一 ~ 九 中文日期
    date_all = re.findall(r'([一二三四五六七八九]日)', line)
    for data in date_all:
        index = line.rindex(data)
        if index + len(data) == len(line):
            line = line[:index]
            # 确定年月
            line, year, month = month_relative_comfirm(line, placeholders_list)
            if year is None:
                line, year, month = month_absolute_comfirm(line, placeholders_list)
            year = now.year if year is None else year
            month = now.month if month is None else month

            # 转成数字
            day = int(day_map[data.replace('日', '')])
            return line, year, month, day

    if len(line) >= 16 and line[-1] in connect_char:
        holder = line[-16:-1]
        if holder in placeholders_list.keys():
            _, time_list = placeholders_list[holder]
            if len(time_list) == 1 and time_list[0] is not None:
                return line[:-1] + '到', time_list[0].year, time_list[0].month, time_list[0].day

    return line, None, None, None
