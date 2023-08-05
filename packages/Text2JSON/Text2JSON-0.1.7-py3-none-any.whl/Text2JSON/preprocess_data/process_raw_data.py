import sys
from os.path import dirname, abspath
path = dirname(dirname(dirname(abspath(__file__))))
sys.path.append(path)
from Text2JSON.train.utils import load_jsonl_by_key, load_jsonl, dump_jsonl
from Text2JSON.entity_named_recog.entity_recognition import entity_recognition


class ProcessedData:
    def __init__(self):
        self.qid = ''
        self.table_id = []
        self.question = ''
        self.tokens = []
        self.char_to_word = []
        self.word_to_char_start = []
        self.sql = {'clause': [], 'relationship': '0'}
        self.valid = ''

    def to_dict(self):
        return {
            'qid': self.qid,
            'table_id': self.table_id,
            'question': self.question,
            'tokens': self.tokens,
            'char_to_word': self.char_to_word,
            'word_to_char_start': self.word_to_char_start,
            'sql': self.sql,
            'valid': self.valid
        }


# 记录WHERE Clause 条件
class Condition:
    def __init__(self, col, op, value):
        self.col = col
        self.op = op
        self.value = value
        self.value_list = value.replace('[', '').replace(']', '').\
            replace('"', '').replace("'", '').replace(' ', '').split(',')

    def parse_with_table(self, op_map, table):
        return [[table['header'].index(self.col), op_map[self.op], len(self.value_list), self.value_list]]


def gen_processed_data(source, target, table_file):
    # 记录操作符映射规则
    # cond_ops = ['=', '!=', '>', '<', '>=', '<=', 'like', 'isnull', 'notnull', 'OP']
    op_map = {'': 0, 'eq': 1, 'not': 2, 'gt': 3, 'lt': 4, 'gte': 5, 'lte': 6, 'like': 7,
              'isnull': 8, 'notnull': 9, 'btw': 10, 'in': 11}
    agg_map = {'': 0, 'eq': 1, 'not': 2, 'gt': 3, 'lt': 4, 'gte': 5, 'lte': 6, 'like': 7,
               'isnull': 8, 'notnull': 9, 'btw': 10, 'in': 11}
    tables = load_jsonl_by_key('url', table_file)
    train_sql_list = []
    for line in load_jsonl(source):
        qid = line['qid']
        question = line['question'].replace(' ', '').strip()
        question = entity_recognition(question)
        tokens = [char for char in question]
        question_tokens = ' '.join(tokens)+' '
        train = ProcessedData()
        train.tokens = tokens
        train.qid = qid

        # do char_to_word
        char_to_word = []
        span = 0
        for i in question_tokens:
            char_to_word.append(span)
            if i == ' ':
                span += 1
        train.char_to_word = char_to_word

        # do word_to_char_start
        space_list = [i for i, x in enumerate(question_tokens) if x == ' ']
        word_to_char_start = [0]
        word_to_char_start.extend([space_list[index] + 1 for index in range(0, len(space_list) - 1)])
        train.word_to_char_start = word_to_char_start

        # 完整query语句
        train.sql['relationship'] = 1 if len(line['query']) == 2 else 0
        try:
            for k in range(0, len(line['query'])):
                temp_query = line['query'][k]
                # 获取表名
                table_name = temp_query['url']
                # 获取表头
                header = [value for value in tables[table_name]['header']]

                # 设置table数据
                train.table_id.append(tables[table_name]['id'])

                # select_clause 所涉及到的列, 默认加上一个占位符, 如果后续不在
                select_list = []
                # select_clause 所涉及到的列集合运算符
                agg_list = []
                # where_clause 所涉及到的列，操作符，值
                cond_list = []

                if 'params' not in temp_query.keys():
                    '不用加占位符'
                else:
                    for l in range(0, len(temp_query['params'])):
                        temp_param = temp_query['params'][l]
                        col = temp_param['name']
                        option = temp_param['option']
                        value = temp_param['value']
                        value_list = value.replace('[', '').replace(']', '').\
                            replace('"', '').replace("'", '').replace(' ', '').split(',')
                        flag = value_in_question(question, value_list)
                        if flag:
                            cond_list.append(Condition(col, option, value))
                        else:
                            for value in value_list:
                                select_list.append(col + '&' + value)
                                agg_list.append(option)

                # 解析sql语句,并且设置train数据
                value_start_end = {}
                sel = [header.index(sel_col) for sel_col in select_list]
                agg = [agg_map[agg] for agg in agg_list]
                conditions = []
                for con in cond_list:
                    conditions.extend(con.parse_with_table(op_map, tables[table_name]))
                for condition in conditions:
                    value_list = condition[3]
                    for value in value_list:
                        value_start_end[value] = find_token_start_end(question_tokens, question, value)
                train.sql['clause'].append({'seq': k, 'sel': sel, 'agg': agg,
                                            'conds': conditions,
                                            'value_start_end': value_start_end})

            # # 设置train数据
            train.question = ' '.join(tokens)+' '
            train.valid = True
            train_sql_list.append(train)
        except ValueError:
            print('数据解析错误, qid={0}的标注数据无法识别'.format(qid))

    # 导出到文件中
    dump_jsonl([sql.to_dict() for sql in train_sql_list], target)


def value_in_question(question, value_list):
    flag = True
    for value in value_list:
        if value in question:
            continue
        else:
            flag = False
            break
    return flag


# 找出token的开始位置和结束位置
def find_token_start_end(question, question_without_token, value):
    if value not in question_without_token:
        return [-1, -1]

    question_list = question.split(' ')
    candidate_token = []
    for index, token in enumerate(question_list):
        if token in value and token != '':
            candidate_token.append([token, index])

    token_list = []
    for pair in candidate_token:
        token = pair[0]
        index = pair[1]
        token_list.append(token)
        sub_token = ''.join(token_list)
        if len(sub_token) < len(value):
            continue
        elif len(sub_token) > len(value):
            length = len(sub_token)
            while length > len(value):
                token_list.pop(0)
                sub_token = ''.join(token_list)
                length = len(sub_token)
        if sub_token == value:
            start_token_index = index - len(token_list) + 1
            # end_token_index = index + 1
            end_token_index = index
            return [start_token_index, end_token_index]

    print('error, 逻辑错误',value,question_without_token)
    return [-1, -1]
