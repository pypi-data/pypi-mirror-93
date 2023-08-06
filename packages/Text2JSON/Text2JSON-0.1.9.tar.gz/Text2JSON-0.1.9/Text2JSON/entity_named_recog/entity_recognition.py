import sys
from os.path import dirname, abspath

path = dirname(dirname(dirname(abspath(__file__))))
sys.path.append(path)
from Text2JSON.entity_named_recog.minute_entity_recognition import minute_recon
from Text2JSON.entity_named_recog.hour_entity_recognition import hour_recon
from Text2JSON.entity_named_recog.day_entity_recognition import day_recon
from Text2JSON.entity_named_recog.month_entity_recognition import month_recon
from Text2JSON.entity_named_recog.quarter_entity_recognition import quart_recon
from Text2JSON.entity_named_recog.year_entity_recognition import year_recon
from Text2JSON.entity_named_recog.proper_noun_recognition import proper_recon
import chinese2digits as ctd
import copy


def entity_recognition(original_line, proper_noun_list=None):
    if proper_noun_list is None:
        proper_noun_list = []
    line = copy.deepcopy(original_line)
    line = line.replace('：', ':')
    line = line.replace(' ', '')
    placeholders_list = {}
    line = proper_recon(line, placeholders_list, proper_noun_list)
    line = minute_recon(line, placeholders_list)
    line = hour_recon(line, placeholders_list)
    line = day_recon(line, placeholders_list)
    line = month_recon(line, placeholders_list)
    line = quart_recon(line, placeholders_list)
    line = year_recon(line, placeholders_list)
    line = ctd.takeChineseNumberFromString(line)['replacedText']
    for holder, data in placeholders_list.items():
        line = line.replace(holder, data[0])
    line = line.replace('““', '“')
    line = line.replace('””', '”')
    return line


def only_parsing_time(original_line, proper_noun_list=None):
    if proper_noun_list is None:
        proper_noun_list = []
    line = copy.deepcopy(original_line)
    line = line.replace('：', ':')
    line = line.replace(' ', '')
    placeholders_list = {}
    line = proper_recon(line, placeholders_list, proper_noun_list)
    line = minute_recon(line, placeholders_list)
    line = hour_recon(line, placeholders_list)
    line = day_recon(line, placeholders_list)
    line = month_recon(line, placeholders_list)
    line = quart_recon(line, placeholders_list)
    line = year_recon(line, placeholders_list)
    for holder, data in placeholders_list.items():
        line = line.replace(holder, data[0])
    line = line.replace('““', '“')
    line = line.replace('””', '”')
    return line


def only_paring_unit(original_line):
    return ctd.takeChineseNumberFromString(original_line)['replacedText']


def entity_recognition_with_value_list(value_list, proper_noun_list=None):
    # 去除不需要解析的专有名词
    if proper_noun_list is None:
        proper_noun_list = []
    paring_index_list = []
    for index, value in enumerate(value_list):
        if value not in proper_noun_list:
            paring_index_list.append(index)

    parsed_result_list = []
    # 如果需要解析的词为空，则直接返回原本的value_list
    if len(paring_index_list) == 0:
        'do nothing'
    # 有可能是时间段
    elif len(paring_index_list) == 2:
        line_1 = only_parsing_time(value_list[paring_index_list[0]], proper_noun_list)
        line_2 = only_parsing_time(value_list[paring_index_list[1]], proper_noun_list)
        # 解析前后没有变化，则不需要做时间解析，只需要做单位解析
        if value_list[paring_index_list[0]] == line_1 and value_list[paring_index_list[1]] == line_2:
            parsed_result_list.append(only_paring_unit(value_list[paring_index_list[0]]))
            parsed_result_list.append(only_paring_unit(value_list[paring_index_list[1]]))
        # 只需要解析第一个时间
        elif value_list[paring_index_list[0]] != line_1 and value_list[paring_index_list[1]] == line_2:
            parsed_result_list.extend([token.replace('“', '').replace('”', '') for token in line_1.split('”到“')])
            parsed_result_list.append(only_paring_unit(value_list[paring_index_list[1]]))
        # 只需要解析第二个
        elif value_list[paring_index_list[0]] == line_1 and value_list[paring_index_list[1]] != line_2:
            parsed_result_list.append(only_paring_unit(value_list[paring_index_list[0]]))
            parsed_result_list.extend([token.replace('“', '').replace('”', '') for token in line_2.split('”到“')])
        else:
            original_line = value_list[paring_index_list[0]] + '到' + value_list[paring_index_list[1]]
            parsed_line = only_parsing_time(original_line, proper_noun_list)
            # 不是时间段
            if original_line == parsed_line:
                'do nothing'
            else:
                parsed_result_list.extend([token.replace('“', '').replace('”', '')
                                           for token in parsed_line.split('”到“')])
    else:
        for index in paring_index_list:
            original_line = value_list[index]
            parsed_line = only_parsing_time(original_line, proper_noun_list)
            if parsed_line == original_line:
                parsed_result_list.append(only_paring_unit(value_list[paring_index_list[index]]))
            else:
                parsed_result_list.extend(
                    [token.replace('“', '').replace('”', '') for token in parsed_line.split('”到“')])
    parsed_value_list = []
    for index, value in enumerate(value_list):
        if index not in paring_index_list:
            parsed_value_list.append(value)
    parsed_value_list.extend(parsed_result_list)
    return parsed_value_list


def test_entity_recognition():
    example1 = "帮我查一下最近1个月内有哪些范本有新的评价"
    line = entity_recognition(example1)
    print(example1)
    print(line)
    example2 = "我创建一个采购办公用品的合同，金额30万"
    line = entity_recognition(example2)
    print(example2)
    print(line)
    example3 = "帮我用办公用品采购合同范本创建一个合同，金额30万，相对方是“北京慧点科技有限公司”"
    line = entity_recognition(example3, ['北京慧点科技有限公司'])
    print(example3)
    print(line)
    example4 = "帮我查一下我10月3日提交的“办公用品采购合同”现在到谁审批了"
    line = entity_recognition(example4)
    print(example4)
    print(line)
    example5 = "我正在执行的合同里有哪些合同的相对方最近1个月发生过风险事件"
    line = entity_recognition(example5)
    print(example5)
    print(line)
    example6 = "帮我查一下今年西安分公司销售合同签订的情况（份数、金额）"
    line = entity_recognition(example6)
    print(example6)
    print(line)
    example7 = "今年发生解除的有哪些合同"
    line = entity_recognition(example7)
    print(example7)
    print(line)
    example8 = "帮我导出一下今年合同的台账"
    line = entity_recognition(example8)
    print(example8)
    print(line)
    example9 = "帮我导出本季度, 西安分公司合同的台账，包含合同名称、合同金额、相对方、合同编号"
    line = entity_recognition(example9)
    print(example9)
    print(line)
    example10 = "今年一共发生了多少案件"
    line = entity_recognition(example10)
    print(example10)
    print(line)
    example11 = "有多少案件今年已经结案"
    line = entity_recognition(example11)
    print(example11)
    print(line)
    example12 = "帮我导出今年新发案件的台账"
    line = entity_recognition(example12)
    print(example12)
    print(line)
    example13 = "帮我查一下最近1个月内，上个月和下一个月有哪些范本有新的评价"
    line = entity_recognition(example13)
    print(example13)
    print(line)
    ''
    example14 = "帮我查一下本季度，上一季度，下一季度，最近一个季度，上季度，下季度"
    line = entity_recognition(example14)
    print(example14)
    print(line)
    example15 = '15年第1季度，2014年第二季度，2021年第三季度，08年第四季度，1998年第二季度，本季度，上季度，下季度，第一季度，第二季度，第3季度，第4季度'
    line = entity_recognition(example15)
    print(example15)
    print(line)
    example16 = '1月，二月，3月，16年2月，17年12月'
    line = entity_recognition(example16)
    print(example16)
    print(line)
    example17 = '帮我订一个会议室，明天上午9：00 - 11: 30，9人参与，要求有投影仪'
    line = entity_recognition(example17)
    print(example17)
    print(line)
    example18 = '凌晨三点，早上六点，上午八点，中午十二点，下午六点，晚上九点，傍晚五点'
    line = entity_recognition(example18)
    print(example18)
    print(line)
    example18 = '晚上九点'
    line = entity_recognition(example18)
    print(example18)
    print(line)
    example19 = '凌晨3点，早上6点，上午8点，中午12点，下午6点，晚上9点，傍晚5点'
    line = entity_recognition(example19)
    print(example19)
    print(line)
    example20 = '凌晨三点二十分，上午八点五十五分，中午十二点十分，下午两点五十五分，晚上九点二十分，傍晚五点半'
    line = entity_recognition(example20)
    print(example20)
    print(line)
    example21 = '凌晨3点，早上6点，上午8点，中午12点，下午6点，晚上9点，傍晚5点'
    line = entity_recognition(example21)
    print(example21)
    print(line)
    example22 = '上午六点五十五分, 早上八点十分， 早上八点零分， 早上八点二十分，早上八点零分'
    line = entity_recognition(example22)
    print(example22)
    print(line)
    example23 = '下午六点五十五分, 傍晚八点十分， 晚上八点零分， 晚上八点十分， 晚上八点零分'
    line = entity_recognition(example23)
    print(example23)
    print(line)
    example24 = '中午十二点五十五分, 正午十一点十分， 正午一点零分， 中午一点十分'
    line = entity_recognition(example24)
    print(example24)
    print(line)
    example24 = '凌晨二点五十五分, 凌晨十一点十分， 凌晨一点零分， 凌晨一点十分'
    line = entity_recognition(example24)
    print(example24)
    print(line)
    example25 = '二点五十五分, 十一点十分， 二十一点零分， 二十四点十分'
    line = entity_recognition(example25)
    print(example25)
    print(line)
    example26 = '二点55分, 十一点10分， 二十一点0分， 二十四点20分'
    line = entity_recognition(example26)
    print(example26)
    print(line)
    example26 = '11日二点55分, 十二日十一点10分， 下一天二十一点0分， 昨天二十四点20分'
    line = entity_recognition(example26)
    print(example26)
    print(line)
    example27 = '十二日十一点10分， 下一天二十一点0分， 昨天二十四点20分'
    line = entity_recognition(example27)
    print(example27)
    print(line)
    example27 = '11日3点55分 - 3点20分'
    line = entity_recognition(example27)
    print(example27)
    print(line)
    example28 = '18年12月11日3点55-4点20'
    line = entity_recognition(example28)
    print(example28)
    print(line)
    example29 = '下午3点五十分'
    line = entity_recognition(example29)
    print(example29)
    print(line)
    example29 = '30分钟后，五分钟后，60分钟前，十分钟前'
    line = entity_recognition(example29)
    print(example29)
    print(line)
    example29 = '5小时前，三十三小时前，14小时后，五小时后'
    line = entity_recognition(example29)
    print(example29)
    print(line)
    example29 = '3天后，十六天后，5天前，十三天前'
    line = entity_recognition(example29)
    print(example29)
    print(line)

    example29 = '3天后下午6点-晚上9点'
    line = entity_recognition(example29)
    print(example29)
    print(line)

    example29 = '下个月6日下午5点30-晚上7点45'
    line = entity_recognition(example29)
    print(example29)
    print(line)

    example29 = '上一季度'
    line = entity_recognition(example29)
    print(example29)
    print(line)

    example29 = '五小时后'
    line = entity_recognition(example29)
    print(example29)
    print(line)

    example29 = '上午9点到10点'
    line = entity_recognition(example29)
    print(example29)
    print(line)


def test_entity_recognition_with_value_list():
    value_list = ['2021年01月28日', '01月29日']
    proper_noun_list = ['一审', '二审', '三审']
    result = entity_recognition_with_value_list(value_list, proper_noun_list)
    print(result)

    value_list = ['一', '二']
    proper_noun_list = ['一审', '二审', '三审']
    result = entity_recognition_with_value_list(value_list, proper_noun_list)
    print(result)

    value_list = ['最近一个月']
    proper_noun_list = ['一审', '二审', '三审']
    result = entity_recognition_with_value_list(value_list, proper_noun_list)
    print(result)

    value_list = ['本季度']
    proper_noun_list = ['一审', '二审', '三审']
    result = entity_recognition_with_value_list(value_list, proper_noun_list)
    print(result)

    value_list = ['第一季度', '第二季度']
    proper_noun_list = ['一审', '二审', '三审']
    result = entity_recognition_with_value_list(value_list, proper_noun_list)
    print(result)

    value_list = ['张三', '第二季度']
    proper_noun_list = ['一审', '二审', '三审', '张三']
    result = entity_recognition_with_value_list(value_list, proper_noun_list)
    print(result)

    value_list = ['2021年01月28日', '2021年01月29日']
    proper_noun_list = ['一审', '二审', '三审']
    result = entity_recognition_with_value_list(value_list, proper_noun_list)
    print(result)

    value_list = ['今天', '明天']
    proper_noun_list = ['一审', '二审', '三审']
    result = entity_recognition_with_value_list(value_list, proper_noun_list)
    print(result)

    value_list = ['明早9点', '12点']
    proper_noun_list = ['一审', '二审', '三审']
    result = entity_recognition_with_value_list(value_list, proper_noun_list)
    print(result)

    value_list = ['AJJJ', 'BJJJ', 'CJJJ', 'DJJJ']
    proper_noun_list = ['一审', '二审', '三审']
    result = entity_recognition_with_value_list(value_list, proper_noun_list)
    print(result)


if __name__ == '__main__':
    # test_entity_recognition()
    test_entity_recognition_with_value_list()
