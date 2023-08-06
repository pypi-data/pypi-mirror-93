import random


def date_to_str(tem_date):
    year = str(tem_date.year)
    month = str(tem_date.month) if len(str(tem_date.month)) == 2 else '0' + str(tem_date.month)
    day = str(tem_date.day) if len(str(tem_date.day)) == 2 else '0' + str(tem_date.day)
    return year + '年' + month + '月' + day + '日'


def time_to_str(tem_date):
    year = str(tem_date.year)
    month = str(tem_date.month) if len(str(tem_date.month)) == 2 else '0' + str(tem_date.month)
    day = str(tem_date.day) if len(str(tem_date.day)) == 2 else '0' + str(tem_date.day)
    hour = str(tem_date.hour) if len(str(tem_date.hour)) == 2 else '0' + str(tem_date.hour)
    minute = str(tem_date.minute) if len(str(tem_date.minute)) == 2 else '0' + str(tem_date.minute)
    return year + '年' + month + '月' + day + '日' + hour + ':' + minute


def random_str(slen=15):
    seed = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
    sa = []
    for i in range(slen):
        sa.append(random.choice(seed))
    return ''.join(sa)
