import sys
from os.path import dirname, abspath
path = dirname(dirname(dirname(abspath(__file__))))
sys.path.append(path)
import datetime
import re
from datetime import date, timedelta
from Text2JSON.entity_named_recog.day_entity_recognition import day_absolute_comfirm, day_relative_comfirm
from Text2JSON.entity_named_recog.entity_utils import *


def hour_recon(line, placeholders_list: dict):
    line = hour_relative_recognition(line, placeholders_list)
    line = hour_absolute_recognition(line, placeholders_list)
    return line


def hour_absolute_recognition(line, placeholders_list: dict):
    time_map = {'零': '0', '一': '1', '二': '2', '三': '3', '四': '4',
                '五': '5', '六': '6', '七': '7', '八': '8', '九': '9', '十': '10', '两': '2'}
    now = date.today()
    # 数字 上午
    date_all_morning_1 = re.findall(r"(上午\d{1,2}点)", line)
    date_all_morning_2 = re.findall(r"(早上\d{1,2}点)", line)
    date_all_morning_3 = re.findall(r"(早\d{1,2}点)", line)
    for data in date_all_morning_1 + date_all_morning_2 + date_all_morning_3:
        index = line.index(data)
        first_line = line[0: index]
        sec_line = line[index + len(data):]
        hour_minute = re.sub(r'(上午)', '', data)
        hour_minute = re.sub(r'(早上)', '', hour_minute)
        hour_minute = re.sub(r'(早)', '', hour_minute)
        hour_minute = hour_minute.replace('点', ':')

        # 确定年月日
        handle_line, year, month, day = day_relative_comfirm(first_line, placeholders_list)
        if year is None:
            handle_line, year, month, day = day_absolute_comfirm(first_line, placeholders_list)
        year = now.year if year is None else year
        month = now.month if month is None else month
        day = now.day if day is None else day

        # 确定小时 和 分钟
        hour = int(hour_minute[:hour_minute.index(':')])
        try:
            # 进一天
            if hour == 24:
                hour = 0
                target_time = datetime.datetime(year, month, day, hour)
                target_time = target_time + timedelta(days=1)
            else:
                target_time = datetime.datetime(year, month, day, hour)
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

    # 数字 下午, 傍晚，晚上
    date_all_afternoon = re.findall(r"(下午\d{1,2}点)", line)
    date_all_nightfall = re.findall(r"([傍]?晚\d{1,2}点)", line)
    date_all_night = re.findall(r"(晚上\d{1,2}点)", line)
    for data in date_all_afternoon + date_all_nightfall + date_all_night:
        index = line.index(data)
        first_line = line[0: index]
        sec_line = line[index + len(data):]
        hour_minute = re.sub(r'(下午)', '', data)
        hour_minute = re.sub(r'(晚上)', '', hour_minute)
        hour_minute = re.sub(r'([傍]?晚)', '', hour_minute)
        hour_minute = hour_minute.replace('点', ':')
        # 确定年月日
        handle_line, year, month, day = day_relative_comfirm(first_line, placeholders_list)
        if year is None:
            handle_line, year, month, day = day_absolute_comfirm(first_line, placeholders_list)
        year = now.year if year is None else year
        month = now.month if month is None else month
        day = now.day if day is None else day

        # 确定小时 和 分钟
        hour = int(hour_minute[:hour_minute.index(':')])
        try:
            # 进一天
            if hour == 24:
                hour = 0
                target_time = datetime.datetime(year, month, day, hour)
                target_time = target_time + timedelta(days=1)
            else:
                target_time = datetime.datetime(year, month, day, hour)
                # 加时间
                if hour <= 12:
                    target_time = target_time + timedelta(hours=12)

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

    # 数字 中午
    date_all_1 = re.findall(r"(中午[01]?[123]点)", line)
    date_all_2 = re.findall(r"(正午[01]?[123]点)", line)
    for data in date_all_1 + date_all_2:
        index = line.index(data)
        first_line = line[0: index]
        sec_line = line[index + len(data):]
        hour_minute = re.sub(r'(中午)', '', data)
        hour_minute = re.sub(r'(正午)', '', hour_minute)
        hour_minute = hour_minute.replace('点', ':')
        # 确定年月日
        handle_line, year, month, day = day_relative_comfirm(first_line, placeholders_list)
        if year is None:
            handle_line, year, month, day = day_absolute_comfirm(first_line, placeholders_list)
        year = now.year if year is None else year
        month = now.month if month is None else month
        day = now.day if day is None else day

        # 确定小时 和 分钟
        hour = int(hour_minute[:hour_minute.index(':')])
        try:
            # 进一天
            if hour == 24:
                hour = 0
                target_time = datetime.datetime(year, month, day, hour)
                target_time = target_time + timedelta(days=1)
            else:
                target_time = datetime.datetime(year, month, day, hour)
                # 加时间
                if hour <= 2:
                    target_time = target_time + timedelta(hours=12)
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

    # 数字 凌晨
    date_all_early = re.findall(r"(凌晨[0]?[123456]点)", line)
    for data in date_all_early:
        index = line.index(data)
        first_line = line[0: index]
        sec_line = line[index + len(data):]
        hour_minute = re.sub(r'(凌晨)', '', data)
        hour_minute = hour_minute.replace('点', ':')
        # 确定年月日
        handle_line, year, month, day = day_relative_comfirm(first_line, placeholders_list)
        if year is None:
            handle_line, year, month, day = day_absolute_comfirm(first_line, placeholders_list)
        year = now.year if year is None else year
        month = now.month if month is None else month
        day = now.day if day is None else day

        # 确定小时 和 分钟
        hour = int(hour_minute[:hour_minute.index(':')])
        try:
            # 进一天
            if hour == 24:
                hour = 0
                target_time = datetime.datetime(year, month, day, hour)
                target_time = target_time + timedelta(days=1)
            else:
                target_time = datetime.datetime(year, month, day, hour)
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

    # 数字
    date_all = re.findall(r"(\d{1,2}点)", line)
    for data in date_all:
        index = line.index(data)
        first_line = line[0: index]
        sec_line = line[index + len(data):]

        hour_minute = data.replace('点', ':')

        # 确定年月日
        handle_line, year, month, day = day_relative_comfirm(first_line, placeholders_list)
        if year is None:
            handle_line, year, month, day = day_absolute_comfirm(first_line, placeholders_list)
        year = now.year if year is None else year
        month = now.month if month is None else month
        day = now.day if day is None else day

        # 确定小时 和 分钟
        hour = int(hour_minute[:hour_minute.index(':')])
        try:
            # 进一天
            if hour == 24:
                hour = 0
                target_time = datetime.datetime(year, month, day, hour)
                target_time = target_time + timedelta(days=1)
            else:
                target_time = datetime.datetime(year, month, day, hour)
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

    # 中文 上午
    date_all_morning_1 = re.findall(r"(上午[二]?[十]?[零两一二三四五六七八九十]点)", line)
    date_all_morning_2 = re.findall(r"(早上[二]?[十]?[零两一二三四五六七八九十]点)", line)
    date_all_morning_3 = re.findall(r"(早[二]?[十]?[零两一二三四五六七八九十]点)", line)
    for data in date_all_morning_1 + date_all_morning_2 + date_all_morning_3:
        index = line.index(data)
        first_line = line[0: index]
        sec_line = line[index + len(data):]
        hour_minute = re.sub(r'(上午)', '', data)
        hour_minute = re.sub(r'(早上)', '', hour_minute)
        hour_minute = re.sub(r'(早)', '', hour_minute)
        hour_minute = re.sub(r'(分)', '', hour_minute)
        hour_minute = re.sub(r'(钟)', '', hour_minute)
        hour_minute = hour_minute.replace('点', ':')

        # 确定年月日
        handle_line, year, month, day = day_relative_comfirm(first_line, placeholders_list)
        if year is None:
            handle_line, year, month, day = day_absolute_comfirm(first_line, placeholders_list)
        year = now.year if year is None else year
        month = now.month if month is None else month
        day = now.day if day is None else day

        # 确定小时 和 分钟
        hour = hour_minute[:hour_minute.index(':')]

        # 解析小时
        if len(hour) > 1:
            if '十' not in hour:
                hour = 25
            else:
                pre_hour = hour[0:hour.index('十')]
                post_hour = hour[hour.index('十') + 1:]
                # 10
                if len(pre_hour) == 0 and len(post_hour) == 0:
                    hour = 10
                # 11 ~ 19
                elif len(pre_hour) == 0 and len(post_hour) != 0:
                    hour = 10 + int(time_map[post_hour])
                # 20, 30
                elif len(pre_hour) != 0 and len(post_hour) == 0:
                    hour = int(time_map[pre_hour]) * 10
                else:
                    # 21 ~ 29
                    hour = int(time_map[pre_hour]) * 10 + int(time_map[post_hour])
        else:
            hour = int(time_map[hour])

        try:
            # 进一天
            if hour == 24:
                target_time = datetime.datetime(year, month, day, 0)
                target_time = target_time + timedelta(days=1)
            else:
                target_time = datetime.datetime(year, month, day, hour)
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

    # 中文 下午
    date_all_afternoon = re.findall(r"(下午[二]?[十]?[两一二三四五六七八九十]点)", line)
    date_all_nightfall = re.findall(r"([傍]?晚[二]?[十]?[两一二三四五六七八九十]点)", line)
    date_all_night = re.findall(r"(晚上[二]?[十]?[两一二三四五六七八九十]点)", line)
    for data in date_all_afternoon + date_all_nightfall + date_all_night:
        index = line.index(data)
        first_line = line[0: index]
        sec_line = line[index + len(data):]
        hour_minute = re.sub(r'(下午)', '', data)
        hour_minute = re.sub(r'(晚上)', '', hour_minute)
        hour_minute = re.sub(r'([傍]?晚)', '', hour_minute)
        hour_minute = re.sub(r'(分)', '', hour_minute)
        hour_minute = re.sub(r'(钟)', '', hour_minute)
        hour_minute = hour_minute.replace('点', ':')

        # 确定年月日
        handle_line, year, month, day = day_relative_comfirm(first_line, placeholders_list)
        if year is None:
            handle_line, year, month, day = day_absolute_comfirm(first_line, placeholders_list)
        year = now.year if year is None else year
        month = now.month if month is None else month
        day = now.day if day is None else day

        # 确定小时 和 分钟
        hour = hour_minute[:hour_minute.index(':')]

        # 解析小时
        if len(hour) > 1:
            if '十' not in hour:
                hour = 25
            else:
                pre_hour = hour[0:hour.index('十')]
                post_hour = hour[hour.index('十') + 1:]
                # 10
                if len(pre_hour) == 0 and len(post_hour) == 0:
                    hour = 10
                # 11 ~ 19
                elif len(pre_hour) == 0 and len(post_hour) != 0:
                    hour = 10 + int(time_map[post_hour])
                # 20, 30
                elif len(pre_hour) != 0 and len(post_hour) == 0:
                    hour = int(time_map[pre_hour]) * 10
                else:
                    # 21 ~ 29
                    hour = int(time_map[pre_hour]) * 10 + int(time_map[post_hour])
        else:
            hour = int(time_map[hour])

        try:
            # 进一天
            if hour == 24:
                target_time = datetime.datetime(year, month, day, 0)
                target_time = target_time + timedelta(days=1)
            else:
                target_time = datetime.datetime(year, month, day, hour)
                # 加时间
                if hour <= 12:
                    target_time = target_time + timedelta(hours=12)
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

    # 中文 中午
    date_all_1 = re.findall(r"(中午十[一二三]点)", line)
    date_all_2 = re.findall(r"(正午十[一二三]点)", line)
    for data in date_all_1 + date_all_2:
        index = line.index(data)
        first_line = line[0: index]
        sec_line = line[index + len(data):]
        hour_minute = re.sub(r'(中午)', '', data)
        hour_minute = re.sub(r'(正午)', '', hour_minute)
        hour_minute = re.sub(r'(分)', '', hour_minute)
        hour_minute = re.sub(r'(钟)', '', hour_minute)
        hour_minute = hour_minute.replace('点', ':')
        # 确定年月日
        handle_line, year, month, day = day_relative_comfirm(first_line, placeholders_list)
        if year is None:
            handle_line, year, month, day = day_absolute_comfirm(first_line, placeholders_list)
        year = now.year if year is None else year
        month = now.month if month is None else month
        day = now.day if day is None else day

        # 确定小时 和 分钟
        hour = hour_minute[:hour_minute.index(':')]

        # 解析小时
        if len(hour) > 1:
            if '十' not in hour:
                hour = 25
            else:
                pre_hour = hour[0:hour.index('十')]
                post_hour = hour[hour.index('十') + 1:]
                # 10
                if len(pre_hour) == 0 and len(post_hour) == 0:
                    hour = 10
                # 11 ~ 19
                elif len(pre_hour) == 0 and len(post_hour) != 0:
                    hour = 10 + int(time_map[post_hour])
                # 20, 30
                elif len(pre_hour) != 0 and len(post_hour) == 0:
                    hour = int(time_map[pre_hour]) * 10
                else:
                    # 21 ~ 29
                    hour = int(time_map[pre_hour]) * 10 + int(time_map[post_hour])
        else:
            hour = int(time_map[hour])

        try:
            # 进一天
            if hour == 24:
                target_time = datetime.datetime(year, month, day, 0)
                target_time = target_time + timedelta(days=1)
            else:
                target_time = datetime.datetime(year, month, day, hour)

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

    # 中文 中午
    date_all_1 = re.findall(r"(中午一点)", line)
    date_all_2 = re.findall(r"(正午一点)", line)
    for data in date_all_1 + date_all_2:
        index = line.index(data)
        first_line = line[0: index]
        sec_line = line[index + len(data):]
        # 确定年月日
        handle_line, year, month, day = day_relative_comfirm(first_line, placeholders_list)
        if year is None:
            handle_line, year, month, day = day_absolute_comfirm(first_line, placeholders_list)
        year = now.year if year is None else year
        month = now.month if month is None else month
        day = now.day if day is None else day

        hour = 13

        try:
            # 进一天
            if hour == 24:
                target_time = datetime.datetime(year, month, day, 0)
                target_time = target_time + timedelta(days=1)
            else:
                target_time = datetime.datetime(year, month, day, hour)
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

    # 中文 凌晨
    date_all_early = re.findall(r"(凌晨[二]?[十]?[一两二三四五六七八九十]点)", line)
    for data in date_all_early:
        index = line.index(data)
        first_line = line[0: index]
        sec_line = line[index + len(data):]
        hour_minute = re.sub(r'(凌晨)', '', data)
        hour_minute = re.sub(r'(分)', '', hour_minute)
        hour_minute = re.sub(r'(钟)', '', hour_minute)
        hour_minute = hour_minute.replace('点', ':')
        # 确定年月日
        handle_line, year, month, day = day_relative_comfirm(first_line, placeholders_list)
        if year is None:
            handle_line, year, month, day = day_absolute_comfirm(first_line, placeholders_list)
        year = now.year if year is None else year
        month = now.month if month is None else month
        day = now.day if day is None else day

        # 确定小时 和 分钟
        hour = int(time_map[hour_minute[:hour_minute.index(':')]])

        try:
            # 进一天
            if hour == 24:
                target_time = datetime.datetime(year, month, day, 0)
                target_time = target_time + timedelta(days=1)
            else:
                target_time = datetime.datetime(year, month, day, hour)
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

    # 数字
    date_all = re.findall(r"([二]?[十]?[两一二三四五六七八九十]点)", line)
    for data in date_all:
        index = line.index(data)
        first_line = line[0: index]
        sec_line = line[index + len(data):]

        hour_minute = re.sub(r'(分)', '', data)
        hour_minute = re.sub(r'(钟)', '', hour_minute)
        hour_minute = hour_minute.replace('点', ':')

        # 确定年月日
        handle_line, year, month, day = day_relative_comfirm(first_line, placeholders_list)
        if year is None:
            handle_line, year, month, day = day_absolute_comfirm(first_line, placeholders_list)
        year = now.year if year is None else year
        month = now.month if month is None else month
        day = now.day if day is None else day

        # 确定小时 和 分钟
        hour = hour_minute[:hour_minute.index(':')]

        # 解析小时
        if len(hour) > 1:
            if '十' not in hour:
                hour = 25
            else:
                pre_hour = hour[0:hour.index('十')]
                post_hour = hour[hour.index('十') + 1:]
                # 10
                if len(pre_hour) == 0 and len(post_hour) == 0:
                    hour = 10
                # 11 ~ 19
                elif len(pre_hour) == 0 and len(post_hour) != 0:
                    hour = 10 + int(time_map[post_hour])
                # 20, 30
                elif len(pre_hour) != 0 and len(post_hour) == 0:
                    hour = int(time_map[pre_hour]) * 10
                else:
                    # 21 ~ 29
                    hour = int(time_map[pre_hour]) * 10 + int(time_map[post_hour])
        else:
            hour = int(time_map[hour])

        try:
            # 进一天
            if hour == 24:
                target_time = datetime.datetime(year, month, day, 0)
                target_time = target_time + timedelta(days=1)
            else:
                target_time = datetime.datetime(year, month, day, hour)
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


def hour_relative_recognition(line, placeholders_list: dict):
    time_map = {'一': '1', '二': '2', '三': '3', '四': '4',
                '五': '5', '六': '6', '七': '7', '八': '8', '九': '9', '两': '2'}
    # 半单独拿出来，放到分钟那里
    now = datetime.datetime.now()

    # 中文前 0-99
    date_all = re.findall(r"([二三四五六七八九]?[十]?[零一二三四五六七八九十半][个]?小时前)", line)
    for data in date_all:
        index = line.index(data)
        first_line = line[0: index]
        sec_line = line[index + len(data):]

        # 计算时差，获取目标时间
        hour = re.sub(r"[个]?小时前", '', data)
        try:
            # 解析小时
            if len(hour) > 1:
                if '十' not in hour:
                    raise ValueError
                else:
                    pre_hour = hour[0:hour.index('十')]
                    post_hour = hour[hour.index('十') + 1:]
                    # 10
                    if len(pre_hour) == 0 and len(post_hour) == 0:
                        hour = 10
                    # 11 ~ 19
                    elif len(pre_hour) == 0 and len(post_hour) != 0:
                        hour = 10 + int(time_map[post_hour])
                    # 20, 30
                    elif len(pre_hour) != 0 and len(post_hour) == 0:
                        hour = int(time_map[pre_hour]) * 10
                    else:
                        # 21 ~ 29
                        hour = int(time_map[pre_hour]) * 10 + int(time_map[post_hour])
            else:
                hour = int(time_map[hour])
        except ValueError:
            # 识别不出来就认为是错误，后续不再识别
            time_str = data
            placeholder = random_str()
            placeholders_list[placeholder] = (time_str, [None])
            line = first_line + placeholder + sec_line
            continue
        target_time = now - timedelta(hours=hour)
        time_str = '“' + time_to_str(target_time) + "”"
        placeholder = random_str()
        placeholders_list[placeholder] = (time_str, [target_time])
        line = first_line + placeholder + sec_line

    # 数字前
    date_all = re.findall(r"(\d{1,2}[个]?小时前)", line)
    for data in date_all:
        index = line.index(data)
        first_line = line[0: index]
        sec_line = line[index + len(data):]
        # 计算时差，获取目标时间
        data = re.sub(r"[个]?小时前", '', data)
        hours_delta = int(data)
        target_time = now - timedelta(hours=hours_delta)
        time_str = '“' + time_to_str(target_time) + "”"
        placeholder = random_str()
        placeholders_list[placeholder] = (time_str, [target_time])
        line = first_line + placeholder + sec_line

    # 中文后 10-99
    date_all = re.findall(r"([二三四五六七八九]?[十]?[零一二三四五六七八九十半][个]?小时后)", line)
    for data in date_all:
        index = line.index(data)
        first_line = line[0: index]
        sec_line = line[index + len(data):]

        # 计算时差，获取目标时间
        data = re.sub(r"[个]?小时后", '', data)
        hour = data
        try:
            # 解析小时
            if len(hour) > 1:
                if '十' not in hour:
                    raise ValueError
                else:
                    pre_hour = hour[0:hour.index('十')]
                    post_hour = hour[hour.index('十') + 1:]
                    # 10
                    if len(pre_hour) == 0 and len(post_hour) == 0:
                        hour = 10
                    # 11 ~ 19
                    elif len(pre_hour) == 0 and len(post_hour) != 0:
                        hour = 10 + int(time_map[post_hour])
                    # 20, 30
                    elif len(pre_hour) != 0 and len(post_hour) == 0:
                        hour = int(time_map[pre_hour]) * 10
                    else:
                        # 21 ~ 29
                        hour = int(time_map[pre_hour]) * 10 + int(time_map[post_hour])
            else:
                hour = int(time_map[hour])
        except ValueError:
            # 识别不出来就认为是错误，后续不再识别
            time_str = data
            placeholder = random_str()
            placeholders_list[placeholder] = (time_str, [None])
            line = first_line + placeholder + sec_line
            continue
        target_time = now + timedelta(hours=hour)
        time_str = '“' + time_to_str(target_time) + "”"
        placeholder = random_str()
        placeholders_list[placeholder] = (time_str, [target_time])
        line = first_line + placeholder + sec_line

    # 数字后
    date_all = re.findall(r"(\d{1,2}[个]?小时后)", line)
    for data in date_all:
        index = line.index(data)
        first_line = line[0: index]
        sec_line = line[index + len(data):]
        # 计算时差，获取目标时间
        data = re.sub(r"[个]?小时后", '', data)
        hours_delta = int(data)
        target_time = now + timedelta(hours=hours_delta)
        time_str = '“' + time_to_str(target_time) + "”"
        placeholder = random_str()
        placeholders_list[placeholder] = (time_str, [target_time])
        line = first_line + placeholder + sec_line

    # 半 前
    date_all = re.findall(r"(半[个]?小时前)", line)
    for data in date_all:
        index = line.index(data)
        first_line = line[0: index]
        sec_line = line[index + len(data):]
        # 计算时差，获取目标时间
        minute_delta = 30
        target_time = now - timedelta(minutes=minute_delta)
        time_str = '“' + time_to_str(target_time) + "”"
        placeholder = random_str()
        placeholders_list[placeholder] = (time_str, [target_time])
        line = first_line + placeholder + sec_line

    # 半 后
    date_all = re.findall(r"(半[个]?小时后)", line)
    for data in date_all:
        index = line.index(data)
        first_line = line[0: index]
        sec_line = line[index + len(data):]
        # 计算时差，获取目标时间
        minute_delta = 30
        target_time = now + timedelta(minutes=minute_delta)
        time_str = '“' + time_to_str(target_time) + "”"
        placeholder = random_str()
        placeholders_list[placeholder] = (time_str, [target_time])
        line = first_line + placeholder + sec_line
    return line


def hour_absolute_comfirm(line, placeholders_list: dict):
    time_map = {'零': '0', '一': '1', '二': '2', '三': '3', '四': '4',
                '五': '5', '六': '6', '七': '7', '八': '8', '九': '9', '十': '10', '两': '2'}
    connect_char = ['-', '~', '到', '至']
    now = date.today()
    # 数字 上午
    date_all_morning_1 = re.findall(r"(上午\d{1,2}[点:])", line)
    date_all_morning_2 = re.findall(r"(早上\d{1,2}[点:])", line)
    for data in date_all_morning_1 + date_all_morning_2:
        index = line.rindex(data)
        if index + len(data) == len(line):
            line = line[:index]

            hour = re.sub(r'(上午)', '', data)
            hour = re.sub(r'(早上)', '', hour)
            hour = re.sub(r'([点:])', '', hour)

            # 确定年月日
            line, year, month, day = day_relative_comfirm(line, placeholders_list)
            if year is None:
                line, year, month, day = day_absolute_comfirm(line, placeholders_list)
            year = now.year if year is None else year
            month = now.month if month is None else month
            day = now.day if day is None else day
            hour = int(hour)
            return line, year, month, day, hour

    # 数字 下午, 傍晚，晚上
    date_all_afternoon = re.findall(r"(下午\d{1,2}[点:])", line)
    date_all_nightfall = re.findall(r"(傍晚\d{1,2}[点:])", line)
    date_all_night = re.findall(r"(晚上\d{1,2}[点:])", line)
    for data in date_all_afternoon + date_all_nightfall + date_all_night:
        index = line.rindex(data)
        if index + len(data) == len(line):
            line = line[:index]

            hour = re.sub(r'(下午)', '', data)
            hour = re.sub(r'(傍晚)', '', hour)
            hour = re.sub(r'(晚上)', '', hour)
            hour = re.sub(r'([点:])', '', hour)

            # 确定年月日
            line, year, month, day = day_relative_comfirm(line, placeholders_list)
            if year is None:
                line, year, month, day = day_absolute_comfirm(line, placeholders_list)
            year = now.year if year is None else year
            month = now.month if month is None else month
            day = now.day if day is None else day
            # 确定小时 和 分钟
            hour = int(hour)
            if hour <= 12:
                hour += 12
            return line, year, month, day, hour

    # 数字 中午
    date_all_1 = re.findall(r"(中午[01]?[123][点:])", line)
    date_all_2 = re.findall(r"(正午[01]?[123][点:])", line)
    for data in date_all_1 + date_all_2:
        index = line.rindex(data)
        if index + len(data) == len(line):
            line = line[:index]

            hour = re.sub(r'(中午)', '', data)
            hour = re.sub(r'(正午)', '', hour)
            hour = re.sub(r'([点:])', '', hour)
            # 确定年月日
            line, year, month, day = day_relative_comfirm(line, placeholders_list)
            if year is None:
                line, year, month, day = day_absolute_comfirm(line, placeholders_list)
            year = now.year if year is None else year
            month = now.month if month is None else month
            day = now.day if day is None else day

            # 确定小时 和 分钟
            hour = int(hour)
            return line, year, month, day, hour

    # 数字 凌晨
    date_all_early = re.findall(r"(凌晨[0]?[123456][点:])", line)
    for data in date_all_early:
        index = line.rindex(data)
        if index + len(data) == len(line):
            line = line[:index]
            hour = re.sub(r'(凌晨)', '', data)
            hour = re.sub(r'([点:])', '', hour)

            # 确定年月日
            line, year, month, day = day_relative_comfirm(line, placeholders_list)
            if year is None:
                line, year, month, day = day_absolute_comfirm(line, placeholders_list)
            year = now.year if year is None else year
            month = now.month if month is None else month
            day = now.day if day is None else day

            # 确定小时 和 分钟
            hour = int(hour)
            return line, year, month, day, hour

    # 数字
    date_all = re.findall(r"(\d{1,2}[点:])", line)
    for data in date_all:
        index = line.rindex(data)
        if index + len(data) == len(line):
            line = line[:index]

            hour = re.sub(r'([点:])', '', data)

            # 确定年月日
            line, year, month, day = day_relative_comfirm(line, placeholders_list)
            if year is None:
                line, year, month, day = day_absolute_comfirm(line, placeholders_list)
            year = now.year if year is None else year
            month = now.month if month is None else month
            day = now.day if day is None else day

            # 确定小时 和 分钟
            hour = int(hour)
            return line, year, month, day, hour

    # 中文 上午
    date_all_morning_1 = re.findall(r"(上午[二]?[十]?[零两一二三四五六七八九十][点:])", line)
    date_all_morning_2 = re.findall(r"(早上[二]?[十]?[零两一二三四五六七八九十][点:])", line)
    for data in date_all_morning_1 + date_all_morning_2:
        index = line.rindex(data)
        if index + len(data) == len(line):
            line = line[:index]
            hour = re.sub(r'(上午)', '', data)
            hour = re.sub(r'(早上)', '', hour)
            hour = re.sub(r'(分)', '', hour)
            hour = re.sub(r'(钟)', '', hour)
            hour = re.sub(r'([点:])', '', hour)

            # 确定年月日
            line, year, month, day = day_relative_comfirm(line, placeholders_list)
            if year is None:
                line, year, month, day = day_absolute_comfirm(line, placeholders_list)
            year = now.year if year is None else year
            month = now.month if month is None else month
            day = now.day if day is None else day

            # 解析小时
            if len(hour) > 1:
                if '十' not in hour:
                    hour = 25
                else:
                    pre_hour = hour[0:hour.index('十')]
                    post_hour = hour[hour.index('十') + 1:]
                    # 10
                    if len(pre_hour) == 0 and len(post_hour) == 0:
                        hour = 10
                    # 11 ~ 19
                    elif len(pre_hour) == 0 and len(post_hour) != 0:
                        hour = 10 + int(time_map[post_hour])
                    # 20, 30
                    elif len(pre_hour) != 0 and len(post_hour) == 0:
                        hour = int(time_map[pre_hour]) * 10
                    else:
                        # 21 ~ 29
                        hour = int(time_map[pre_hour]) * 10 + int(time_map[post_hour])
            else:
                hour = int(time_map[hour])
            return line, year, month, day, hour

    # 中文 下午
    date_all_afternoon = re.findall(r"(下午[二]?[十]?[两一二三四五六七八九十][点:])", line)
    date_all_nightfall = re.findall(r"(傍晚[二]?[十]?[两一二三四五六七八九十][点:])", line)
    date_all_night = re.findall(r"(晚上[二]?[十]?[两一二三四五六七八九十][点:])", line)
    for data in date_all_afternoon + date_all_nightfall + date_all_night:
        index = line.rindex(data)
        if index + len(data) == len(line):
            line = line[:index]

            hour = re.sub(r'(下午)', '', data)
            hour = re.sub(r'(傍晚)', '', hour)
            hour = re.sub(r'(晚上)', '', hour)
            hour = re.sub(r'(分)', '', hour)
            hour = re.sub(r'(钟)', '', hour)
            hour = re.sub(r'([点:])', '', hour)

            # 确定年月日
            line, year, month, day = day_relative_comfirm(line, placeholders_list)
            if year is None:
                line, year, month, day = day_absolute_comfirm(line, placeholders_list)
            year = now.year if year is None else year
            month = now.month if month is None else month
            day = now.day if day is None else day

            # 解析小时
            if len(hour) > 1:
                if '十' not in hour:
                    hour = 25
                else:
                    pre_hour = hour[0:hour.index('十')]
                    post_hour = hour[hour.index('十') + 1:]
                    # 10
                    if len(pre_hour) == 0 and len(post_hour) == 0:
                        hour = 10
                    # 11 ~ 19
                    elif len(pre_hour) == 0 and len(post_hour) != 0:
                        hour = 10 + int(time_map[post_hour])
                    # 20, 30
                    elif len(pre_hour) != 0 and len(post_hour) == 0:
                        hour = int(time_map[pre_hour]) * 10
                    else:
                        # 21 ~ 29
                        hour = int(time_map[pre_hour]) * 10 + int(time_map[post_hour])
            else:
                hour = int(time_map[hour])
            if hour <= 12:
                hour += 12
            return line, year, month, day, hour

    # 中文 中午
    date_all_1 = re.findall(r"(中午十[一二三][点:])", line)
    date_all_2 = re.findall(r"(正午十[一二三][点:])", line)
    for data in date_all_1 + date_all_2:
        index = line.rindex(data)
        if index + len(data) == len(line):
            line = line[:index]

            hour = re.sub(r'(中午)', '', data)
            hour = re.sub(r'(正午)', '', hour)
            hour = re.sub(r'(分)', '', hour)
            hour = re.sub(r'(钟)', '', hour)
            hour = re.sub(r'([点:])', '', hour)

            # 确定年月日
            line, year, month, day = day_relative_comfirm(line, placeholders_list)
            if year is None:
                line, year, month, day = day_absolute_comfirm(line, placeholders_list)
            year = now.year if year is None else year
            month = now.month if month is None else month
            day = now.day if day is None else day

            # 解析小时
            if len(hour) > 1:
                if '十' not in hour:
                    hour = 25
                else:
                    pre_hour = hour[0:hour.index('十')]
                    post_hour = hour[hour.index('十') + 1:]
                    # 10
                    if len(pre_hour) == 0 and len(post_hour) == 0:
                        hour = 10
                    # 11 ~ 19
                    elif len(pre_hour) == 0 and len(post_hour) != 0:
                        hour = 10 + int(time_map[post_hour])
                    # 20, 30
                    elif len(pre_hour) != 0 and len(post_hour) == 0:
                        hour = int(time_map[pre_hour]) * 10
                    else:
                        # 21 ~ 29
                        hour = int(time_map[pre_hour]) * 10 + int(time_map[post_hour])
            else:
                hour = int(time_map[hour])
            return line, year, month, day, hour

    # 中文 中午
    date_all_1 = re.findall(r"(中午一[点:])", line)
    date_all_2 = re.findall(r"(正午一[点:])", line)
    for data in date_all_1 + date_all_2:
        index = line.rindex(data)
        if index + len(data) == len(line):
            line = line[:index]

            # 确定年月日
            line, year, month, day = day_relative_comfirm(line, placeholders_list)
            if year is None:
                line, year, month, day = day_absolute_comfirm(line, placeholders_list)
            year = now.year if year is None else year
            month = now.month if month is None else month
            day = now.day if day is None else day

            hour = 13
            return line, year, month, day, hour

    # 中文 凌晨
    date_all_early = re.findall(r"(凌晨[二]?[十]?[一两二三四五六七八九十][点:])", line)
    for data in date_all_early:
        index = line.rindex(data)
        if index + len(data) == len(line):
            line = line[:index]

            hour = re.sub(r'(凌晨)', '', data)
            hour = re.sub(r'(分)', '', hour)
            hour = re.sub(r'(钟)', '', hour)
            hour = re.sub(r'([点:])', '', hour)

            # 确定年月日
            line, year, month, day = day_relative_comfirm(line, placeholders_list)
            if year is None:
                line, year, month, day = day_absolute_comfirm(line, placeholders_list)
            year = now.year if year is None else year
            month = now.month if month is None else month
            day = now.day if day is None else day

            # 解析小时
            if len(hour) > 1:
                if '十' not in hour:
                    hour = 25
                else:
                    pre_hour = hour[0:hour.index('十')]
                    post_hour = hour[hour.index('十') + 1:]
                    # 10
                    if len(pre_hour) == 0 and len(post_hour) == 0:
                        hour = 10
                    # 11 ~ 19
                    elif len(pre_hour) == 0 and len(post_hour) != 0:
                        hour = 10 + int(time_map[post_hour])
                    # 20, 30
                    elif len(pre_hour) != 0 and len(post_hour) == 0:
                        hour = int(time_map[pre_hour]) * 10
                    else:
                        # 21 ~ 29
                        hour = int(time_map[pre_hour]) * 10 + int(time_map[post_hour])
            else:
                hour = int(time_map[hour])
            return line, year, month, day, hour

    # 数字
    date_all = re.findall(r"([二]?[十]?[两一二三四五六七八九十][点:])", line)
    for data in date_all:
        index = line.rindex(data)
        if index + len(data) == len(line):
            line = line[:index]

            hour = re.sub(r'(分)', '', data)
            hour = re.sub(r'(钟)', '', hour)
            hour = re.sub(r'([点:])', '', hour)

            # 确定年月日
            line, year, month, day = day_relative_comfirm(line, placeholders_list)
            if year is None:
                line, year, month, day = day_absolute_comfirm(line, placeholders_list)
            year = now.year if year is None else year
            month = now.month if month is None else month
            day = now.day if day is None else day

            # 解析小时
            if len(hour) > 1:
                if '十' not in hour:
                    hour = 25
                else:
                    pre_hour = hour[0:hour.index('十')]
                    post_hour = hour[hour.index('十') + 1:]
                    # 10
                    if len(pre_hour) == 0 and len(post_hour) == 0:
                        hour = 10
                    # 11 ~ 19
                    elif len(pre_hour) == 0 and len(post_hour) != 0:
                        hour = 10 + int(time_map[post_hour])
                    # 20, 30
                    elif len(pre_hour) != 0 and len(post_hour) == 0:
                        hour = int(time_map[pre_hour]) * 10
                    else:
                        # 21 ~ 29
                        hour = int(time_map[pre_hour]) * 10 + int(time_map[post_hour])
            else:
                hour = int(time_map[hour])
            return line, year, month, day, hour

    if len(line) >= 16 and line[-1] in connect_char:
        holder = line[-16:-1]
        if holder in placeholders_list.keys():
            _, time_list = placeholders_list[holder]
            if len(time_list) == 1 and time_list[0] is not None:
                return line[:-1] + '到', time_list[0].year, time_list[0].month, time_list[0].day, time_list[0].hour

    return line, None, None, None, None
