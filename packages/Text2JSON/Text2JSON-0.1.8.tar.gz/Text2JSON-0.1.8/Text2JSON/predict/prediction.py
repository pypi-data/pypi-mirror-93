import sys
from os.path import dirname, abspath

path = dirname(dirname(dirname(abspath(__file__))))
sys.path.append(path)
import json
import numpy as np
import os
from Text2JSON.model.base_model import BaseModel
from Text2JSON.featurizer.schema_featurizer import SchemaDataset
from Text2JSON.featurizer.column_featurizer import ColumnDataset
from Text2JSON.featurizer.Input_SQL import SQLExample
from Text2JSON.train.utils import dump_model, load_model

op_map = {'': 0, 'eq': 1, 'not': 2, 'gt': 3, 'lt': 4, 'gte': 5, 'lte': 6, 'like': 7,
          'isnull': 8, 'notnull': 9, 'btw': 10, 'in': 11}
agg_map = {'': 0, 'eq': 1, 'not': 2, 'gt': 3, 'lt': 4, 'gte': 5, 'lte': 6, 'like': 7,
           'isnull': 8, 'notnull': 9, 'btw': 10, 'in': 11}

agg_map_reverse = {0: '', 1: 'eq', 2: 'not', 3: 'gt', 4: 'lt', 5: 'gte', 6: 'lte', 7: 'like', 8: 'isnull', 9: 'notnull',
                   10: 'btw', 11: 'in'}
op_map_reverse = {0: '', 1: 'eq', 2: 'not', 3: 'gt', 4: 'lt', 5: 'gte', 6: 'lte', 7: 'like', 8: 'isnull', 9: 'notnull',
                  10: 'btw', 11: 'in'}


class request_template(object):
    def __init__(self, method, url, params):
        self.method = method
        self.url = url
        self.params = params

    def to_dict(self):
        return {
            'method': self.method,
            'url': self.url,
            'params': self.params
        }


class GenJSON(object):
    def __init__(self, config, schema_data, column_data, schema, model1, model2):
        self.config = config
        self.schema_data = schema_data
        self.column_data = column_data
        self.schema = schema
        self.model1 = model1
        self.model2 = model2

    def gen_json(self, question, first_json=1, sec_json=1, qid=0, size=50):
        self.config['schema_evaluator_batch_size'] = size
        self.config['column_evaluator_batch_size'] = size
        example = self.question_pre_handle(question, qid)
        self.schema_data.load_for_predict(example, True)
        schema_model_outputs = self.model1.dataset_inference(self.schema_data)

        # SQL1 relative
        first_table_relevant_prob = np.exp(schema_model_outputs[0]['schema_first_sim'][:, 0])
        first_table_id_prob_exp = sorted(enumerate(first_table_relevant_prob), key=lambda x: x[1], reverse=True)
        first_table_rel = []
        for table_index, table_pro in first_table_id_prob_exp:
            if table_pro >= float(self.config['schema_threshold']):
                first_table_rel.append(table_index)
                if len(first_table_rel) == int(self.config['schema_remain']):
                    break

        # SQL2 relative
        sec_table_relevant_prob = np.exp(schema_model_outputs[0]['schema_sec_sim'][:, 0])
        sec_table_id_prob_exp = sorted(enumerate(sec_table_relevant_prob), key=lambda x: x[1], reverse=True)
        sec_table_rel = []
        for table_index, table_pro in sec_table_id_prob_exp:
            if table_pro >= float(self.config['schema_threshold']):
                sec_table_rel.append(table_index)
                if len(first_table_rel) == int(self.config['schema_remain']):
                    break

        result = None
        # 先不考虑剪枝
        if len(first_table_rel) == 0:
            result = {'qid': qid, 'question': question, 'query': []}
        # 两句SQL
        else:
            # zip SQL1 and SQL2
            example.first_schema_id = [self.schema.table_global_to_local[index] for index in first_table_rel]
            example.sec_schema_id = [self.schema.table_global_to_local[index] for index in sec_table_rel]
            self.column_data.load_for_predict(example, True)

            # 用于标识两个语句的关系
            # model output SQL
            column_model_outputs = self.model2.dataset_inference(self.column_data)
            for sql1_index, first_schema_id in enumerate(first_table_rel):
                first_relation, sec_relation = None, None
                if sql1_index == int(first_json):
                    break
                first_schema_id = self.schema.table_global_to_local[first_schema_id]
                input_feature = self.column_data.input_features[sql1_index]
                model_output = column_model_outputs[sql1_index]
                first_request, first_relation = self.sql_parser(self.model2, first_schema_id, input_feature,
                                                                model_output, 0)
                if len(sec_table_rel) == 0:
                    result = {'qid': qid, 'question': question, 'query': [first_request.to_dict()]}
                    continue
                for sql2_index, sec_schema_id in enumerate(sec_table_rel):
                    if sql2_index == int(sec_json):
                        break
                    sec_schema_id = self.schema.table_global_to_local[sec_schema_id]
                    input_feature = self.column_data.input_features[len(first_table_rel) + sql2_index]
                    model_output = column_model_outputs[len(first_table_rel) + sql2_index]
                    sec_request, sec_relation = self.sql_parser(self.model2, sec_schema_id, input_feature, model_output,
                                                                1)

                    # 剪枝
                    if first_request.url == sec_request.url:
                        # 只要第一句
                        result = {'qid': qid, 'question': question, 'query': [first_request.to_dict()]}
                    elif first_relation == 0 and sec_relation == 0:
                        # 只要第一句
                        result = {'qid': qid, 'question': question, 'query': [first_request.to_dict()]}
                    else:
                        # 两句都要
                        result = {'qid': qid, 'question': question,
                                  'query': [first_request.to_dict(), sec_request.to_dict()]}
        return result

    def question_pre_handle(self, line, qid):
        """
            qid
            question
            table_id
            tokens
            word_to_char_start
        """

        example = SQLExample()
        example.qid = qid
        example.table_id = None
        line = line.replace(' ', '')
        tokens = [char for char in line]
        example.tokens = tokens
        example.question = line

        space_list = [i for i, x in enumerate(' '.join(tokens)) if x == ' ']
        word_to_char_start = [0]
        word_to_char_start.extend([space_list[index] + 1 for index in range(0, len(space_list) - 1)])
        example.word_to_char_start = word_to_char_start
        return example

    def generate_json(self, model: BaseModel, input_feature, model_output, sql_seq=0):
        """
            predict sql on dataset
            dataset: 需要预测的数据
            model_outputs: 数据经过模型预测后的输出
        """
        stop_word_list = ['【', '】', '[', ']', '"', "'", '‘', '’', '“', '，', '.', '。', ' ', '”']

        sel, agg, where, _, conditions, relationship = model. \
            parse_output_with_threshold(input_feature, model_output, sql_seq, float(self.config['column_threshold']))
        conditions_with_value_texts = []
        for wc in where:
            _, op, span_list = conditions[wc]
            # 通过subword_to_word获取对应的token的start_index, end_index
            value_span_text = []
            for se in span_list:
                # 获取是第几个词
                start_index = se[0]
                end_index = se[1]
                if start_index >= len(input_feature.subword_to_word[wc]):
                    start_index = len(input_feature.subword_to_word[wc]) - 1
                if end_index >= len(input_feature.subword_to_word[wc]):
                    end_index = len(input_feature.subword_to_word[wc]) - 1
                word_start = input_feature.subword_to_word[wc][start_index]
                word_end = input_feature.subword_to_word[wc][end_index] + 1
                span = ''.join(input_feature.tokens_common[word_start:word_end]).rstrip()
                for stop_word in stop_word_list:
                    if stop_word in span:
                        span.replace(stop_word, '')
                value_span_text.append(span)
            conditions_with_value_texts.append((wc, op, value_span_text))

        # 将agg,select, conditions封装到sql中
        return sel, agg, conditions_with_value_texts, relationship

    def parse_params(self, schema_id, sel, agg, conditions_with_value_texts):
        # 遍历SQL语句
        params = []
        select_params = []
        where_params = []

        # 这里可以进行剪枝，看看select 有没有出现在 where 中，或者反过来
        for index, sel_col_index in enumerate(sel):
            col_name_value = self.schema.extend_schema[schema_id]['header'][sel_col_index]
            if '&' not in col_name_value:
                '去除占位符'
                continue
            col_name = col_name_value.split('&')[0]
            col_value = col_name_value.split('&')[1]

            agg_name = agg_map_reverse[agg[index][1]]
            if agg_name == 'in' or agg_name == 'btw':
                col_value = '"' + col_value + '"'
            select_params.append((col_name, agg_name, col_value))

        for where_col_index, op_index, value_list in conditions_with_value_texts:
            col_name = self.schema.extend_schema[schema_id]['header'][where_col_index]
            op_name = op_map_reverse[op_index]
            if len(value_list) >= 2:
                for value_index, value in enumerate(value_list):
                    value = value_list[value_index]
                    value = value.replace('”', '')
                    value = value.replace('"', '')
                    value_list[value_index] = '"' + str(value) + '"'
                value = value_list
            else:
                value = value_list[0]
                value = value.replace('”', '')
                value = value.replace('"', '')
                value = ['"' + str(value) + '"']
            where_params.append((col_name, op_name, value))

        # 合并同类项
        select_name_agg = {}
        select_name_value = {}
        for col_name, agg_name, col_value in select_params:
            if col_name not in select_name_agg.keys():
                select_name_agg[col_name] = [agg_name]
            else:
                select_name_agg[col_name].append(agg_name)
            if col_name not in select_name_value.keys():
                select_name_value[col_name] = [col_value]
            else:
                select_name_value[col_name].append(col_value)

        # 对agg进行剪枝, 选择可能性最大的agg
        for key in select_name_agg.keys():
            if len(select_name_agg[key]) == 1:
                continue
            else:
                agg_name_num = {}
                for agg_name in select_name_agg[key]:
                    if agg_name not in agg_name_num.keys():
                        agg_name_num[agg_name] = 1
                    else:
                        agg_name_num[agg_name] += 1
                if len(agg_name_num.keys()) == 1:
                    continue
                find_max = -1
                max_agg_name = None
                for agg_name in agg_name_num.keys():
                    if agg_name_num[agg_name] > find_max:
                        find_max = agg_name_num[agg_name]
                        max_agg_name = agg_name
                # 这里引入的特征
                if max_agg_name == 'eq' and len(select_name_value[key]) > 1:
                    select_name_agg[key] = ['in']
                else:
                    select_name_agg[key] = [max_agg_name]

        params = []
        # 解析成JSON格式
        for col_name in select_name_agg.keys():
            params.append({'name': col_name, 'option': select_name_agg[col_name][0],
                           'value': str(select_name_value[col_name]) if len(select_name_value[col_name]) > 1
                                                                        or select_name_agg[col_name][0] == 'in'
                           else str(select_name_value[col_name][0])})
        for col_name, op_name, value in where_params:
            if op_name != 'in' and len(value) == 1:
                value = value[0].replace('"', '')
            params.append({'name': col_name, 'option': op_name, 'value': str(value)})

        return params

    def get_url_method(self, table_id):
        url = self.schema.extend_schema[table_id]['url']
        method = self.schema.url_method[url]
        return url, method

    def sql_parser(self, model: BaseModel, schema_id, input_feature, model_output, sql_seq):
        sel, agg, conditions_with_value_texts, relationship = self.generate_json(model, input_feature, model_output,
                                                                                 sql_seq)
        # parsing params
        params = self.parse_params(schema_id, sel, agg, conditions_with_value_texts)
        # get url and method
        url, method = self.get_url_method(schema_id)
        # request
        return request_template(method, url, params), self.first_or_sec(relationship)

    def first_or_sec(self, relationship):
        if len(relationship) == 0:
            return 0
        first = 0
        sec = 0
        for index, rel in relationship:
            if rel == 0:
                first += 1
            else:
                sec += 1
        return 0 if first > sec else 1


def load_test_data(data_path):
    question_list = []
    for line in open(data_path, encoding="utf8"):
        data = json.loads(line)
        question_list.append((data['qid'], data['question'].replace(' ', '')))
    return question_list


class Predict(object):
    def __init__(self):
        # 设置参数
        self.config = None
        # 词编码器
        self.tokenizer = None
        # schema特征提取器
        self.schema_featurizer = None
        # column特征提取器
        self.column_featurizer = None
        # 加载数据表
        self.schema = None
        # schema模型
        self.model1 = None
        # column模型
        self.model2 = None
        # 数据加载器
        self.schema_data = None
        self.column_data = None
        # 预测器
        self.prediction = None

    def set_params(self, config, tokenizer, schema_featurizer, column_featurizer, schema,
                   schema_model, column_model):
        # 设置参数
        self.config = config
        # 词编码器
        self.tokenizer = tokenizer
        # schema特征提取器
        self.schema_featurizer = schema_featurizer
        # column特征提取器
        self.column_featurizer = column_featurizer
        # 加载数据表
        self.schema = schema
        # 选择模型, 加载模型
        self.model1 = schema_model
        self.model2 = column_model

        # 数据加载器
        self.schema_data = SchemaDataset(self.config, self.schema_featurizer, self.schema)
        self.column_data = ColumnDataset(self.config, self.column_featurizer, self.schema)

        # 预测器
        self.prediction = GenJSON(self.config, self.schema_data, self.column_data, self.schema, self.model1,
                                  self.model2)

    def load_to_gpu(self):
        self.model1.to_gpu()
        self.model2.to_gpu()
        self.config['has_cuda'] = True

    def load_to_cpu(self):
        self.model1.to_cpu()
        self.model2.to_cpu()
        self.config['has_cuda'] = False

    def load_model(self, model_path):
        model = load_model(model_path)
        # 设置参数
        self.config = model.config
        # 词编码器
        self.tokenizer = model.tokenizer
        # schema特征提取器
        self.schema_featurizer = model.schema_featurizer
        # column特征提取器
        self.column_featurizer = model.column_featurizer
        # 加载数据表
        self.schema = model.schema
        # 选择模型, 加载模型
        self.model1 = model.model1
        self.model2 = model.model2
        # 数据加载器
        self.schema_data = model.schema_data
        self.column_data = model.column_data
        # 预测器
        self.prediction = model.prediction
        self.config['has_cuda'] = False

    def dump_model(self, model_path):
        dump_model(self, model_path)
        print('Client model saved in path {0}'.format(model_path))

    def predict(self, question, first_sql=1, sec_sql=1, qid=0, size=50):
        return self.prediction.gen_json(question, first_sql, sec_sql, qid, size)
