import sys
from os.path import dirname, abspath
path = dirname(dirname(dirname(abspath(__file__))))
sys.path.append(path)
import datetime
from datetime import date, timedelta
import calendar
from Text2JSON.entity_named_recog.entity_utils import *
from Text2JSON.entity_named_recog.year_entity_recognition import year_absolute_comfirm, year_relative_comfirm


def quart_recon(line, placeholders_list: dict):
    return quarter_relative_absolute_recognition(line, placeholders_list)


def quarter_relative_absolute_recognition(line, placeholders_list: dict):
    cur_quarter = ['最近一个季度', '近一个季度', '最近1个季度', '近1个季度', '近季度', '本季度', '这个季度']
    next_quarter = ['下1个季度', '下一个季度', '下季度', '下个季度', '下季度', '下一季度', '下1季度', '一个季度后', '1个季度后']
    last_quarter = ['上1个季度', '上一个季度', '上季度', '上个季度', '上季度', '上一季度', '上1季度', '一个季度前', '1个季度前']
    first_quarter = ['第一季度', '第1季度', '一季度', '1季度']  # 最长匹配，最长的放在前面
    sec_quarter = ['第二季度', '第2季度', '二季度', '2季度']
    third_quarter = ['第三季度', '第3季度', '三季度', '3季度']
    fourth_quarter = ['第四季度', '第4季度', '四季度', '4季度', '最后一个季度', '最后1个季度']
    first_half_year = ['上半年']
    sec_half_year = ['下半年']
    flag = True
    while flag:
        flag = False
        for quarter in cur_quarter:
            if quarter in line:
                index = line.index(quarter)
                first_line = line[0: index]
                sec_line = line[index + len(quarter):]

                now = date.today()
                # 季度开始月份, 季度结束月份, 季度开始时间, 季度结束时间
                month_start = (now.month - 1) - (now.month - 1) % 3 + 1
                month_end = month_start + 2
                cur_quarter_start = datetime.datetime(now.year, month_start, 1)
                cur_quarter_end = datetime.datetime(now.year, month_end, calendar.monthrange(now.year, month_end)[1])
                time_str = '“' + date_to_str(cur_quarter_start) + '”' + '到' + '“' + date_to_str(cur_quarter_end) + '”'
                placeholder = random_str()
                placeholders_list[placeholder] = (time_str, [cur_quarter_start, cur_quarter_end])
                line = first_line + placeholder + sec_line
                flag = True
                break

        for quarter in next_quarter:
            if quarter in line:
                index = line.index(quarter)
                first_line = line[0: index]
                sec_line = line[index + len(quarter):]

                now = date.today()
                # 思路，先获取本季度的结束月份最后天，日+1，再获取下一个季度的开始和结束时间
                month_start = (now.month - 1) - (now.month - 1) % 3 + 1
                month_end = month_start + 2
                this_quarter_end = datetime.datetime(now.year, month_end, calendar.monthrange(now.year, month_end)[1])

                # 季度开始月份, 季度结束月份, 季度开始时间, 季度结束时间
                next_quarter_temp = (this_quarter_end + timedelta(days=1))
                next_quarter_start_year = next_quarter_temp.year
                next_quarter_start_month = (next_quarter_temp.month - 1) - (next_quarter_temp.month - 1) % 3 + 1
                next_quarter_end_month = next_quarter_start_month + 2

                next_quarter_start = datetime.datetime(next_quarter_start_year, next_quarter_start_month, 1)
                next_quarter_end = datetime.datetime(next_quarter_start_year, next_quarter_end_month,
                                                     calendar.monthrange(next_quarter_start_year,
                                                                         next_quarter_end_month)[1])

                time_str = '“' + date_to_str(next_quarter_start) + '”' + '到' + '“' + date_to_str(next_quarter_end) + '”'
                placeholder = random_str()
                placeholders_list[placeholder] = (time_str, [next_quarter_start, next_quarter_end])
                line = first_line + placeholder + sec_line
                flag = True
                break

        for quarter in last_quarter:
            if quarter in line:
                index = line.index(quarter)
                first_line = line[0: index]
                sec_line = line[index + len(quarter):]

                now = date.today()
                # 思路，先获取本季度的开始月份第一天，日-1，再获取上一个季度的开始和结束时间
                month_start = (now.month - 1) - (now.month - 1) % 3 + 1
                this_quarter_start = datetime.datetime(now.year, month_start, 1)

                # 季度开始月份, 季度结束月份, 季度开始时间, 季度结束时间
                last_quarter_temp = (this_quarter_start + timedelta(days=-1))
                last_quarter_start_year = last_quarter_temp.year
                last_quarter_start_month = (last_quarter_temp.month - 1) - (last_quarter_temp.month - 1) % 3 + 1
                pre_quarter_end_month = last_quarter_start_month + 2

                last_quarter_start = datetime.datetime(last_quarter_start_year, last_quarter_start_month, 1)
                last_quarter_end = datetime.datetime(last_quarter_start_year, pre_quarter_end_month,
                                                     calendar.monthrange(last_quarter_start_year,
                                                                         pre_quarter_end_month)[1])

                time_str = '“' + date_to_str(last_quarter_start) + '”' + '到' + '“' + date_to_str(last_quarter_end) + '”'
                placeholder = random_str()
                placeholders_list[placeholder] = (time_str, [last_quarter_start, last_quarter_end])
                line = first_line + placeholder + sec_line
                flag = True
                break

        for quarter in first_quarter:
            if quarter in line:
                index = line.index(quarter)
                first_line = line[0: index]
                sec_line = line[index + len(quarter):]

                now = date.today()
                # 确定年份
                first_line, year = year_absolute_comfirm(first_line, placeholders_list)
                if year is None:
                    first_line, year = year_relative_comfirm(first_line, placeholders_list)

                year = now.year if year is None else year

                this_quarter_start = datetime.datetime(year, 1, 1)
                this_quarter_end = datetime.datetime(year, 3, 31)
                time_str = '“' + date_to_str(this_quarter_start) + '”' + '到' + '“' + date_to_str(this_quarter_end) + '”'
                placeholder = random_str()
                placeholders_list[placeholder] = (time_str, [this_quarter_start, this_quarter_end])
                line = first_line + placeholder + sec_line
                flag = True
                break

        for quarter in sec_quarter:
            if quarter in line:
                index = line.index(quarter)
                first_line = line[0: index]
                sec_line = line[index + len(quarter):]

                now = date.today()
                # 确定年份
                first_line, year = year_absolute_comfirm(first_line, placeholders_list)
                if year is None:
                    first_line, year = year_relative_comfirm(first_line, placeholders_list)
                year = now.year if year is None else year
                this_quarter_start = datetime.datetime(year, 4, 1)
                this_quarter_end = datetime.datetime(year, 6, 30)
                time_str = '“' + date_to_str(this_quarter_start) + '”' + '到' + '“' + date_to_str(this_quarter_end) + '”'
                placeholder = random_str()
                placeholders_list[placeholder] = (time_str, [this_quarter_start, this_quarter_end])
                line = first_line + placeholder + sec_line
                flag = True
                break

        for quarter in third_quarter:
            if quarter in line:
                index = line.index(quarter)
                first_line = line[0: index]
                sec_line = line[index + len(quarter):]

                now = date.today()
                # 确定年份
                first_line, year = year_absolute_comfirm(first_line, placeholders_list)
                if year is None:
                    first_line, year = year_relative_comfirm(first_line, placeholders_list)
                year = now.year if year is None else year
                this_quarter_start = datetime.datetime(year, 7, 1)
                this_quarter_end = datetime.datetime(year, 9, 30)
                time_str = '“' + date_to_str(this_quarter_start) + '”' + '到' + '“' + date_to_str(this_quarter_end) + '”'
                placeholder = random_str()
                placeholders_list[placeholder] = (time_str, [this_quarter_start, this_quarter_end])
                line = first_line + placeholder + sec_line
                flag = True
                break

        for quarter in fourth_quarter:
            if quarter in line:
                index = line.index(quarter)
                first_line = line[0: index]
                sec_line = line[index + len(quarter):]

                now = date.today()
                # 确定年份
                first_line, year = year_absolute_comfirm(first_line, placeholders_list)
                if year is None:
                    first_line, year = year_relative_comfirm(first_line, placeholders_list)
                year = now.year if year is None else year
                this_quarter_start = datetime.datetime(year, 10, 1)
                this_quarter_end = datetime.datetime(year, 12, 31)
                time_str = '“' + date_to_str(this_quarter_start) + '”' + '到' + '“' + date_to_str(this_quarter_end) + '”'
                placeholder = random_str()
                placeholders_list[placeholder] = (time_str, [this_quarter_start, this_quarter_end])
                line = first_line + placeholder + sec_line
                flag = True
                break

        for first_half in first_half_year:
            if first_half in line:
                index = line.index(first_half)
                first_line = line[0: index]
                sec_line = line[index + len(first_half):]

                now = date.today()
                # 确定年份
                first_line, year = year_absolute_comfirm(first_line, placeholders_list)
                if year is None:
                    first_line, year = year_relative_comfirm(first_line, placeholders_list)
                year = now.year if year is None else year
                this_half_start = datetime.datetime(year, 1, 1)
                this_half_end = datetime.datetime(year, 6, 30)
                time_str = '“' + date_to_str(this_half_start) + '”' + '到' + '“' + date_to_str(this_half_end) + '”'
                placeholder = random_str()
                placeholders_list[placeholder] = (time_str, [this_half_start, this_half_end])
                line = first_line + placeholder + sec_line
                flag = True
                break

        for sec_half in sec_half_year:
            if sec_half in line:
                index = line.index(sec_half)
                first_line = line[0: index]
                sec_line = line[index + len(sec_half):]

                now = date.today()
                # 确定年份
                first_line, year = year_absolute_comfirm(first_line, placeholders_list)
                if year is None:
                    first_line, year = year_relative_comfirm(first_line, placeholders_list)
                year = now.year if year is None else year
                this_half_start = datetime.datetime(year, 7, 1)
                this_half_end = datetime.datetime(year, 12, 31)
                time_str = '“' + date_to_str(this_half_start) + '”' + '到' + '“' + date_to_str(this_half_end) + '”'
                placeholder = random_str()
                placeholders_list[placeholder] = (time_str, [this_half_start, this_half_end])
                line = first_line + placeholder + sec_line
                flag = True
                break

    return line


if __name__ == '__main__':
    ''
    # example1 = '12年第1季度，16年第二季度，2017年第三季度，2019年第四季度，最近一个季度，上季度，下季度'
    # example2 = '今年第一季度，去年第二季度，明年第三季度，第四季度'
    # example3 = '17年上半年，下半年，今年下半年，明年上半年'
    # sentence, placeholders = quarter_relatice_absolute_recon(example1)
    # for token, holder in placeholders:
    #     sentence = sentence.replace(holder, token)
    # print(sentence)
    # sentence, placeholders = quarter_relatice_absolute_recon(example2)
    # for token, holder in placeholders:
    #     sentence = sentence.replace(holder, token)
    # print(sentence)
    # sentence, placeholders = quarter_relatice_absolute_recon(example3)
    # for token, holder in placeholders:
    #     sentence = sentence.replace(holder, token)
    # print(sentence)
