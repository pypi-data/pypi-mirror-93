import sys
from os.path import dirname, abspath
path = dirname(dirname(dirname(abspath(__file__))))
sys.path.append(path)
from Text2JSON.train.utils import load_jsonl, dump_jsonl, read_vocab, ranking_by_length
from Text2JSON.entity_named_recog.entity_recognition import entity_recognition, entity_recognition_with_value_list


class RawSchema(object):
    def __init__(self):
        self.id = None
        self.method = None
        self.url = None
        self.url_note = ''
        self.params = {}

    def to_dict(self):
        return {
            'id': self.id,
            'method': self.method,
            'url': self.url,
            'url_note': self.url_note,
            'params': [param.to_dict() for param in self.params.values()]
        }


class RawParam(object):
    def __init__(self):
        self.param_name = None
        self.param_note = ''
        self.value_type = None
        self.value_space = None
        self.value_range = []
        self.value_note = []

    def to_dict(self):
        return {
            'param_name': self.param_name,
            'param_note': self.param_note,
            'value_type': self.value_type,
            'value_space': self.value_space,
            'value_range': self.value_range,
            'value_note': self.value_note
        }


# 将完整的URL作为一个表名
def extract(source: list, target, proper_noun_file_list):
    # 读取专有名词
    proper_noun_list = []
    for file_path in proper_noun_file_list:
        proper_noun_list.extend(read_vocab(file_path))
    # 按长度进行排序，保证最长匹配优先
    proper_noun_list = ranking_by_length(proper_noun_list)
    cnt = 1
    schema_dict = {}
    for data in source:
        for line in load_jsonl(data):
            question = entity_recognition(line['question'], proper_noun_list)
            for query in line['query']:
                schema_name = query['url']
                method = query['method']
                if schema_name not in schema_dict.keys():
                    now_schema = RawSchema()
                    now_schema.id = str(cnt)
                    now_schema.url = schema_name
                    now_schema.method = method.upper()
                    schema_dict[schema_name] = now_schema
                    cnt += 1
                else:
                    now_schema = schema_dict[schema_name]
                if 'params' not in query.keys():
                    continue
                for param in query['params']:
                    param_name = param['name'].strip()
                    if param_name == 'order':
                        continue
                    value_list = param['value'].replace('[', '').replace(']', '').replace('"', '').split(',')
                    value_list = entity_recognition_with_value_list(value_list, proper_noun_list)
                    flag = value_in_question(question, value_list)
                    if flag:
                        if param_name in now_schema.params.keys():
                            continue
                        now_param = RawParam()
                        now_param.param_name = param_name
                        now_param.param_note = ''
                        now_param.value_space = 'open'
                        if 'time' in param_name:
                            now_param.value_type = 'date'
                        elif 'amount' in param_name or 'number' in param_name:
                            now_param.value_type = 'number'
                        else:
                            now_param.value_type = 'string'
                        now_schema.params[param_name] = now_param
                    else:
                        if param_name in now_schema.params.keys():
                            now_param = now_schema.params[param_name]
                            for value in value_list:
                                if value not in now_param.value_range:
                                    now_param.value_range.append(value)
                                    now_param.value_note.append('')
                        else:
                            now_param = RawParam()
                            now_param.param_name = param_name
                            now_param.param_note = ''
                            now_param.value_type = 'string'
                            now_param.value_space = 'closed'
                            for value in value_list:
                                now_param.value_range.append(value)
                                now_param.value_note.append('')
                            now_schema.params[param_name] = now_param
    data = []
    for value in schema_dict.values():
        data.append(value.to_dict())
    dump_jsonl(data, target)


def value_in_question(question, value_list):
    flag = True
    for value in value_list:
        if value in question:
            continue
        else:
            flag = False
            break
    return flag
