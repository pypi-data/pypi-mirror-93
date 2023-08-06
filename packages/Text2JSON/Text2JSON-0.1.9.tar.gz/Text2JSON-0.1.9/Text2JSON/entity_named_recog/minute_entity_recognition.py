import sys
from os.path import dirname, abspath
path = dirname(dirname(dirname(abspath(__file__))))
sys.path.append(path)
import datetime
import re
from datetime import timedelta
from Text2JSON.entity_named_recog.hour_entity_recognition import hour_absolute_comfirm
from Text2JSON.entity_named_recog.entity_utils import *


def minute_recon(line, placeholders_list: dict):
    line = minute_relative_recognition(line, placeholders_list)
    line = minute_absolute_recognition(line, placeholders_list)
    return line


def minute_absolute_recognition(line, placeholders_list: dict):
    now = datetime.datetime.now()
    time_map = {'零': '0', '一': '1', '二': '2', '三': '3', '四': '4',
                '五': '5', '六': '6', '七': '7', '八': '8', '九': '9', '十': '10', '两': '2', '半':'30'}
    # 数字 分钟
    date_all = re.findall(r"([:点]\d{1,2}[分]?[钟]?)", line)
    for data in date_all:
        data = data[1:]
        index = line.index(data)
        first_line = line[0: index]
        sec_line = line[index + len(data):]

        minute = re.sub(r'([分]?[钟]?)', '', data)

        # 确定年月日
        handle_line, year, month, day, hour = hour_absolute_comfirm(first_line, placeholders_list)

        year = now.year if year is None else year
        month = now.month if month is None else month
        day = now.day if day is None else day
        hour = now.hour if hour is None else hour

        # 确定分钟
        minute = int(minute)
        try:
            if minute > 60:
                raise ValueError
            if hour > 24:
                raise ValueError

            target_time = datetime.datetime(year, month, day, 0, 0)
            target_time = target_time + timedelta(minutes=minute)
            target_time = target_time + timedelta(hours=hour)
        except ValueError:
            # 识别不出来就认为是错误，后续不再识别
            time_str = data
            placeholder = random_str()
            placeholders_list[placeholder] = (time_str, [None])
            line = first_line + placeholder + sec_line
            continue
        assert target_time is not None, '逻辑错误'
        time_str = '“' + time_to_str(target_time) + "”"
        placeholder = random_str()
        placeholders_list[placeholder] = (time_str, [target_time])
        line = handle_line + placeholder + sec_line

    # 数字 分钟
    date_all = re.findall(r"([:点][二三四五六七八九]?[十]?[零一二三四五六七八九十半][分]?[钟]?)", line)
    for data in date_all:
        data = data[1:]
        index = line.index(data)
        first_line = line[0: index]
        sec_line = line[index + len(data):]

        minute = re.sub(r'([分]?[钟]?)', '', data)

        # 确定年月日
        handle_line, year, month, day, hour = hour_absolute_comfirm(first_line, placeholders_list)

        year = now.year if year is None else year
        month = now.month if month is None else month
        day = now.day if day is None else day
        hour = now.hour if hour is None else hour

        # 解析分钟
        if len(minute) > 1:
            if '十' not in minute:
                # 错误处理
                minute = 61
            else:
                pre_minute = minute[0:minute.index('十')]
                post_minute = minute[minute.index('十') + 1:]
                # 10
                if len(pre_minute) == 0 and len(post_minute) == 0:
                    minute = 10
                # 11 ~ 19
                elif len(pre_minute) == 0 and len(post_minute) != 0:
                    minute = 10 + int(time_map[post_minute])
                # 20, 30
                elif len(pre_minute) != 0 and len(post_minute) == 0:
                    minute = int(time_map[pre_minute]) * 10
                else:
                    # 21 ~ 24
                    minute = int(time_map[pre_minute]) * 10 + int(time_map[post_minute])
        else:
            minute = int(time_map[minute])

        # 确定分钟
        try:
            if minute > 60:
                raise ValueError
            if hour > 24:
                raise ValueError

            target_time = datetime.datetime(year, month, day, 0, 0)
            target_time = target_time + timedelta(minutes=minute)
            target_time = target_time + timedelta(hours=hour)
        except ValueError:
            # 识别不出来就认为是错误，后续不再识别
            time_str = data
            placeholder = random_str()
            placeholders_list[placeholder] = (time_str, [None])
            line = first_line + placeholder + sec_line
            continue
        assert target_time is not None, '逻辑错误'
        time_str = '“' + time_to_str(target_time) + "”"
        placeholder = random_str()
        placeholders_list[placeholder] = (time_str, [target_time])
        line = handle_line + placeholder + sec_line
    return line


def minute_relative_recognition(line, placeholders_list: dict):
    time_map = {'一': '1', '二': '2', '三': '3', '四': '4',
                '五': '5', '六': '6', '七': '7', '八': '8', '九': '9', '两': '2', '十': '10'}
    # 半单独拿出来，放到分钟那里
    now = datetime.datetime.now()
    # 中文前 1-99
    date_all = re.findall(r"([二三四五六七八九]?[十]?[一两二三四五六七八九十]分钟前)", line)
    for data in date_all:
        index = line.index(data)
        first_line = line[0: index]
        sec_line = line[index + len(data):]

        # 计算时差，获取目标时间
        minute = re.sub(r"分钟前", '', data)
        try:
            # 解析分钟
            if len(minute) > 1:
                if '十' not in minute:
                    # 错误处理
                    raise ValueError
                else:
                    pre_minute = minute[0:minute.index('十')]
                    post_minute = minute[minute.index('十') + 1:]
                    # 10
                    if len(pre_minute) == 0 and len(post_minute) == 0:
                        minute = 10
                    # 11 ~ 19
                    elif len(pre_minute) == 0 and len(post_minute) != 0:
                        minute = 10 + int(time_map[post_minute])
                    # 20, 30
                    elif len(pre_minute) != 0 and len(post_minute) == 0:
                        minute = int(time_map[pre_minute]) * 10
                    else:
                        # 21 ~ 24
                        minute = int(time_map[pre_minute]) * 10 + int(time_map[post_minute])
            else:
                minute = int(time_map[minute])
        except ValueError:
            # 识别不出来就认为是错误，后续不再识别
            time_str = data
            placeholder = random_str()
            placeholders_list[placeholder] = (time_str, [None])
            line = first_line + placeholder + sec_line
            continue
        target_time = now - timedelta(minutes=minute)
        time_str = '“' + time_to_str(target_time) + "”"
        placeholder = random_str()
        placeholders_list[placeholder] = (time_str, [target_time])
        line = first_line + placeholder + sec_line

    # 数字前
    date_all = re.findall(r"(\d{1,2}分钟前)", line)
    for data in date_all:
        index = line.index(data)
        first_line = line[0: index]
        sec_line = line[index + len(data):]
        # 计算时差，获取目标时间
        data = re.sub(r"分钟前", '', data)
        minute_delta = int(data)
        target_time = now - timedelta(minutes=minute_delta)
        time_str = '“' + time_to_str(target_time) + "”"
        placeholder = random_str()
        placeholders_list[placeholder] = (time_str, [target_time])
        line = first_line + placeholder + sec_line

    # 中文后 10-99
    date_all = re.findall(r"([二三四五六七八九]?[十]?[一两二三四五六七八九十]分钟后)", line)
    for data in date_all:
        index = line.index(data)
        first_line = line[0: index]
        sec_line = line[index + len(data):]

        # 计算时差，获取目标时间
        minute = re.sub(r"分钟后", '', data)

        try:
            # 解析分钟
            if len(minute) > 1:
                if '十' not in minute:
                    raise ValueError
                else:
                    pre_minute = minute[0:minute.index('十')]
                    post_minute = minute[minute.index('十') + 1:]
                    # 10
                    if len(pre_minute) == 0 and len(post_minute) == 0:
                        minute = 10
                    # 11 ~ 19
                    elif len(pre_minute) == 0 and len(post_minute) != 0:
                        minute = 10 + int(time_map[post_minute])
                    # 20, 30
                    elif len(pre_minute) != 0 and len(post_minute) == 0:
                        minute = int(time_map[pre_minute]) * 10
                    else:
                        # 21 ~ 24
                        minute = int(time_map[pre_minute]) * 10 + int(time_map[post_minute])
            else:
                minute = int(time_map[minute])
        except ValueError:
            # 识别不出来就认为是错误，后续不再识别
            time_str = data
            placeholder = random_str()
            placeholders_list[placeholder] = (time_str, [None])
            line = first_line + placeholder + sec_line
            continue

        target_time = now + timedelta(minutes=minute)
        time_str = '“' + time_to_str(target_time) + "”"
        placeholder = random_str()
        placeholders_list[placeholder] = (time_str, [target_time])
        line = first_line + placeholder + sec_line

    # 数字后
    date_all = re.findall(r"(\d{1,2}分钟后)", line)
    for data in date_all:
        index = line.index(data)
        first_line = line[0: index]
        sec_line = line[index + len(data):]
        # 计算时差，获取目标时间
        data = re.sub(r"分钟后", '', data)
        minute_delta = int(data)
        target_time = now + timedelta(minutes=minute_delta)
        time_str = '“' + time_to_str(target_time) + "”"
        placeholder = random_str()
        placeholders_list[placeholder] = (time_str, [target_time])
        line = first_line + placeholder + sec_line
    return line
