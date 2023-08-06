import sys
from os.path import dirname, abspath
path = dirname(dirname(dirname(abspath(__file__))))
sys.path.append(path)
import numpy as np
import torch.utils.data as torch_data
from Text2JSON.featurizer.schema_parser import schema_parsed
from Text2JSON.featurizer.Input_SQL import SQLExample
from collections import defaultdict

stats = defaultdict(int)


class SchemaInputFeature(object):
    def __init__(self, qid, question, schema_id, relative_schema_id):
        self.qid = qid
        self.question = question
        self.schema_id = schema_id
        self.relative_schema_id = relative_schema_id
        self.tokens = []
        # 用于训练和测试
        self.input_ids = []
        self.input_mask = []
        self.segment_ids = []
        self.schema_rel = []
        self.schema_mask = []

        # 用于测试
        self.schema_sec_rel = []

    def to_dict(self):
        return {
            'qid': self.qid,
            'question': self.question,
            'schema_id': self.schema_id,
            'relative_schema_id': self.relative_schema_id,
            'tokens': self.tokens,
            'input_ids': self.input_ids,
            'input_mask': self.input_mask,
            'segment_ids': self.segment_ids,
            'table_rel': self.schema_rel,
            'mask': self.schema_mask
        }


class HydraSchemaFeaturizer(object):
    """
        特征提取器，将一条训练数据集，转变成为InputFeature
    """

    def __init__(self, config, tokenizer):
        self.config = config
        # 根据不同模型，设置tokenizer
        self.tokenizer = tokenizer

    def get_input_schema_feature(self, example: SQLExample, schema: schema_parsed, config, positive=True, negative=True,
                                note=False):
        max_query_length = int(config["max_query_length"])
        max_column_length = int(config["max_column_length"])
        max_total_length = max_column_length + max_query_length

        # 一条feature包含一条train,包含多个<>column<>question<>编码
        input_feature = SchemaInputFeature(
            example.qid,
            example.question,
            example.table_id,
            example.table_id_relative,
        )

        # 记录映射关系
        tokens = []
        word_to_subword_base = []  # 词 到 子词 的映射关系,形式(start_index, end_index)
        subword_to_word_base = []  # 子词 到 词 的映射关系,形式(0,1,1,2,2,2)
        for i, query_token in enumerate(example.tokens):
            sub_tokens = self.tokenizer.tokenize(query_token)
            cur_pos = len(tokens)
            if len(sub_tokens) > 0:
                word_to_subword_base += [(cur_pos, cur_pos + len(sub_tokens))]
                tokens.extend(sub_tokens)
                subword_to_word_base.extend([i] * len(sub_tokens))

        # positive 只加载正例， negative 只加载负例， 两个都为true，一起加载
        # 遍历表中所有columns，为每一个column生成<>column<>question<>编码
        # 这里只要是表相关的都作为正例
        rel_table = [example.table_id]
        # 是否需要对输入进行拓展
        if note:
            feature_type = 'feature_schema'

        else:
            feature_type = 'feature_schema_without_note'

        for key, value in schema.extend_schema.items():
            # 只要正例
            if positive and not negative:
                if key not in rel_table:
                    continue
            # 只要负例
            elif not positive and negative:
                if key in rel_table:
                    continue

            # 正例和负例都要
            elif positive and negative:
                ''

            table = schema.extend_schema[key]
            for table_column_feature in table[feature_type]:
                # 编码，输入为type, table, column, table_note, column_note, space, token
                # 输出[cls]type, table, column, table_note, column_note, space[SEP]question[SEP]
                assert len(
                    table_column_feature) <= max_column_length, "{0} URL中参数特征长度过大，请缩小参数参数特征或将配置文件中的" \
                                                                "max_column_length增大".format(table['url'])
                assert len(''.join(
                    tokens)) <= max_query_length, '问句: {0} 输入问句长度大于最大字符长度，请将配置文件中的max_query_length' \
                                                  '增大或者缩短输入问句长度'.format(example.question)
                tokenize_result = self.tokenizer.encode_plus(
                    table_column_feature,
                    tokens,
                    max_length=max_total_length,
                    truncation_strategy="longest_first",
                    pad_to_max_length=True,
                )

                input_ids = tokenize_result["input_ids"]  # 将输入tokens, 通过词表转换成id
                segment_ids = tokenize_result["token_type_ids"]  # 标识column和question位置[0,0,1,1]
                input_mask = tokenize_result["attention_mask"]  # 标识column+question位置编码,也就是整个输入所占的编码
                new_tokens = self.tokenizer.convert_ids_to_tokens(input_ids)  # 获取编码后的序列[cls]column[SEP]question[SEP]

                assert len(input_ids) == max_total_length
                assert len(input_mask) == max_total_length
                assert len(segment_ids) == max_total_length

                input_feature.tokens.append(new_tokens)
                input_feature.input_ids.append(input_ids)
                input_feature.input_mask.append(input_mask)
                input_feature.segment_ids.append(segment_ids)

        return input_feature

    def get_predict_input_schema_feature(self, example: SQLExample, schema: schema_parsed, config, note=True):
        max_query_length = int(config["max_query_length"])
        max_column_length = int(config["max_column_length"])
        max_total_length = max_column_length + max_query_length

        # 一条feature包含一条train,包含多个<>column<>question<>编码
        input_feature = SchemaInputFeature(
            example.qid,
            example.question,
            example.table_id,
            example.table_id_relative
        )

        # 记录映射关系
        tokens = []
        word_to_subword_base = []  # 词 到 子词 的映射关系,形式(start_index, end_index)
        subword_to_word_base = []  # 子词 到 词 的映射关系,形式(0,1,1,2,2,2)
        for i, query_token in enumerate(example.tokens):
            sub_tokens = self.tokenizer.tokenize(query_token)
            cur_pos = len(tokens)
            if len(sub_tokens) > 0:
                word_to_subword_base += [(cur_pos, cur_pos + len(sub_tokens))]
                tokens.extend(sub_tokens)
                subword_to_word_base.extend([i] * len(sub_tokens))

        # 是否需要对输入进行拓展
        if note:
            feature_type = 'feature_schema'

        else:
            feature_type = 'feature_schema_without_note'

        for key, value in schema.extend_schema.items():
            table = schema.extend_schema[key]
            for table_column_feature in table[feature_type]:
                # 编码，输入为type, table, column, table_note, column_note, space, token
                # 输出[cls]type, table, column, table_note, column_note, space[SEP]question[SEP]
                assert len(table_column_feature) <= max_column_length, "列特征长度过小，请将配置文件中的max_column_length增大"
                assert len(''.join(tokens)) <= max_query_length, "输入问句长度大于最大字符长度，请将配置文件中的max_query_length" \
                                                                 "增大或者缩短输入问句长度"
                tokenize_result = self.tokenizer.encode_plus(
                    table_column_feature,
                    tokens,
                    max_length=max_total_length,
                    truncation_strategy="longest_first",
                    pad_to_max_length=True,
                )

                input_ids = tokenize_result["input_ids"]  # 将输入tokens, 通过词表转换成id
                segment_ids = tokenize_result["token_type_ids"]  # 标识column和question位置[0,0,1,1]
                input_mask = tokenize_result["attention_mask"]  # 标识column+question位置编码,也就是整个输入所占的编码
                new_tokens = self.tokenizer.convert_ids_to_tokens(input_ids)  # 获取编码后的序列[cls]column[SEP]question[SEP]

                assert len(input_ids) == max_total_length, 'input_ids, 错误'
                assert len(input_mask) == max_total_length, 'input_mask, 错误'
                assert len(segment_ids) == max_total_length, 'segment_ids, 错误'

                input_feature.tokens.append(new_tokens)
                input_feature.input_ids.append(input_ids)
                input_feature.input_mask.append(input_mask)
                input_feature.segment_ids.append(segment_ids)

        return input_feature

    def fill_label_schema_feature_split(self, example: SQLExample, input_feature: SchemaInputFeature,
                                       schema: schema_parsed, positive=True, negative=True):
        # 只要正例,对应训练
        if positive and not negative:
            global_table_id = 0
        # 只要负例，对应训练
        elif not positive and negative:
            global_table_id = None
        # 正例和负例都要,对应测试
        elif positive and negative:
            global_table_id = schema.table_local_to_global[str(example.table_id)]
        else:
            assert False, 'Positive 和 Negative 不能全为负'

        # set schema number
        schema_num = len(input_feature.input_ids)  # 表的数量

        # set schema relative
        input_feature.schema_rel = [0] * schema_num
        if global_table_id is not None:
            input_feature.schema_rel[global_table_id] = 1

        # set mask
        input_feature.schema_mask = [example.seq] * schema_num

        return True

    # 加载数据
    def load_schema_data(self, data_paths, config, schema, include_label=False, positive=True, negative=True,
                         note=False):
        '''
            data_paths: 数据路径
            config: 模型参数设置
            include_label: 是否包含标记label
        '''
        # 将input,封装到model_input 中
        # 每一条数据是<>col<>question<>的特征
        model_inputs = {k: [] for k in ["input_ids", "input_mask", "segment_ids"]}
        # 拓展
        if include_label:
            for k in ['schema_rel', 'schema_mask']:
                model_inputs[k] = []

        # 记录输入每一个question所对应的特征序列
        pos = []
        # 多条<>column<>question<>特征
        input_features = []

        # 支持多个数据集
        for data_path in data_paths.split("|"):
            cnt = 0
            for line in open(data_path, encoding="utf8"):
                # 加载一个样本, 一行里面包含一个问句，一个问句有可能对应两个SQL，按SQL进行拆分，拆分成两个样本
                # 将所有正负样本标记在一起
                for index, example in enumerate(SQLExample.load_from_json(line)):
                    # 丢弃未经过验证并且包含sql_label的数据
                    if not example.valid and include_label == True:
                        continue

                    # 获取输入特征,返回一个对象，里面封装了多个<col,question>,<col,question>
                    input_feature = self.get_input_schema_feature(example, schema, config, positive, negative, note)

                    # 如果包含sql_label, 则需要填充特征
                    if include_label:
                        success = self.fill_label_schema_feature_split(example, input_feature, schema, positive,
                                                                       negative)
                        if not success:
                            continue

                    input_features.append(input_feature)  # 总特征

                    # 当前模型有多少个特征
                    cur_start = len(model_inputs["input_ids"])
                    # 当前样本输入有多少个输入特征
                    cur_sample_num = len(input_feature.input_ids)
                    # 标记当前输入模型对应特征的开始和结束位置
                    pos.append((cur_start, cur_start + cur_sample_num))

                    model_inputs["input_ids"].extend(input_feature.input_ids)
                    model_inputs["input_mask"].extend(input_feature.input_mask)
                    model_inputs["segment_ids"].extend(input_feature.segment_ids)
                    if include_label:
                        model_inputs['schema_rel'].extend(input_feature.schema_rel)
                        model_inputs['schema_mask'].extend(input_feature.schema_mask)
                    else:
                        # 如果 include_label is False，则说明这是预测时用的数据，那么只需要一条特征就行了
                        # 因为可以对一条特征进行两次预测，分别是SQL1 和 SQL2
                        break
                    cnt += 1
                    if cnt % 5000 == 0:
                        print('featuring:', cnt)


        '''
            input_features : 数据的特征，可以认为是label
            model_inputs : 数据输入
            pos :  一条数据与多条<>column<>question<>的对应关系
        '''
        return input_features, model_inputs, pos

    # 加载数据
    def load_schema_predict_data(self, example: SQLExample, config, schema, note=True):
        '''
            data_paths: 数据路径
            config: 模型参数设置
            include_label: 是否包含标记label
        '''
        # 将input,封装到model_input 中
        # 每一条数据是<>col<>question<>的特征
        model_inputs = {k: [] for k in ["input_ids", "input_mask", "segment_ids"]}

        # 记录输入每一个question所对应的特征序列
        pos = []
        # 多条<>column<>question<>特征
        input_features = []

        # 获取输入特征,返回一个对象，里面封装了多个<col,question>,<col,question>
        input_feature = self.get_predict_input_schema_feature(example, schema, config, note)

        input_features.append(input_feature)  # 总特征

        # 当前模型有多少个特征
        cur_start = len(model_inputs["input_ids"])
        # 当前样本输入有多少个输入特征
        cur_sample_num = len(input_feature.input_ids)
        # 标记当前输入模型对应特征的开始和结束位置
        pos.append((cur_start, cur_start + cur_sample_num))

        model_inputs["input_ids"].extend(input_feature.input_ids)
        model_inputs["input_mask"].extend(input_feature.input_mask)
        model_inputs["segment_ids"].extend(input_feature.segment_ids)

        '''
            input_features : 数据的特征，可以认为是label
            model_inputs : 数据输入
            pos :  一条数据与多条<>column<>question<>的对应关系
        '''
        return input_features, model_inputs, pos


class SchemaDataset(torch_data.Dataset):
    def __init__(self,  config, featurizer: HydraSchemaFeaturizer, schema):
        self.config = config
        self.featurizer = featurizer
        self.schema = schema
        self.input_features = None
        self.model_inputs = None
        self.pos = None

    def loads(self, data_paths, include_label=False, positive=True, negative=True, note=False):
        self.input_features, self.model_inputs, self.pos = self.featurizer.load_schema_data(data_paths,
                                                                                            self.config,
                                                                                            self.schema,
                                                                                            include_label,
                                                                                            positive,
                                                                                            negative,
                                                                                            note)
        self.trans_data_type()
        print("file {0} loaded".format(data_paths))

    def load_for_predict(self, example, note=True):
        self.input_features, self.model_inputs, self.pos = self.featurizer.load_schema_predict_data(example,
                                                                                                    self.config,
                                                                                                    self.schema,
                                                                                                    note)
        self.trans_data_type()

    # 转换数据类型
    def trans_data_type(self):
        for k in self.model_inputs:
            self.model_inputs[k] = np.array(self.model_inputs[k], dtype=np.int64)

    # 这两个函数是dataloader的关键
    def __len__(self):
        return self.model_inputs["input_ids"].shape[0]

    def __getitem__(self, idx):
        return {k: v[idx] for k, v in self.model_inputs.items()}


if __name__ == "__main__":
    ''
