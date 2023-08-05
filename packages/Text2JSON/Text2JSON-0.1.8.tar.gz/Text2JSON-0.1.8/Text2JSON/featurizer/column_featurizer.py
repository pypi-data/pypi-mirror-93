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


class ColumnInputFeature(object):
    def __init__(self,
                 qid,
                 question,
                 table_id,
                 tokens,
                 word_to_char_start,
                 word_to_subword,
                 subword_to_word,
                 input_ids,
                 input_mask,
                 segment_ids):
        """
            qid: question id
            question: question token 单个
            table_id: table id 单个
            tokens: [[cls]type,column[SEP]question[SEP],...] 一组 column和question的联合表示，获取编码后的序列
            word_to_char_start: [start1, start2, start3, start4] 一组 记录问题token字符的开始位置
            word_to_subword: [[(start_index, end_index),...,],...,[]] 一组 词 到 子词 的映射关系,形式
            subword_to_word: [[0,1,1,2,2,2],...] 一组 子词 到 词 的映射关系
            input_ids: [[id1, id2, id3,..., pad, pad],...] 一组 将输入tokens, 通过词表转换成id
            input_mask: [[1,1,1,1],...] 一组 标识column+question位置编码,也就是整个输入所占的编码
            segment_ids: [[0,0,1,1],...] 一组 标识column和question位置
            columns: [name1, name2, name3, name4, name5] question有可能所涉及到的列
            seq: [0, 0, 0, 0, 0] 位置信息0代表第一条SQL语句，1代表第二条SQL语句
            sel_num: [1, 1, 1, 1, 1] select_clause 对应列的数目
            sel: [0,0,1,0,0] select_clause 所选择的列
            agg: [0, 0, 1, 0, 0]有可能所涉及到的列对应操作符
            where_num: [1, 1, 1, 1, 1] 每一个<>column<>question<> pair 对应的列数目, [len(conds)] * columns
            where: [0, 0, 1, 0, 0] 记录每一个列是否出现在where_clause中
            op: [0, 0, 2, 0, 0] 记录在where_clause中，每一个列对应的操作符
            value_num: [1, 2, 3, 0, 0] where子句中列对应值的数目
            value_start: [[0,...], [0,...], [start_pos1, start_pos2,...], ...] 记录在where_clause中，每一个列对应值在tokens的开始位置, 如果没有，记为-1
            value_end: [[0], [0], [end_pos1, end_pos2] , [0], [0]] 记录在where_clause中，每一个列对应值在tokens的结束位置, 如果没有，记为-1
            relationship: [0, 0, 0, 0, 0] 结构信息 0:代表单条SQL 1:代表两条条SQL
        """
        self.qid = qid
        self.question = question
        self.table_id = table_id
        self.tokens = tokens

        # 这三个都可能没有用
        self.word_to_char_start = word_to_char_start
        self.word_to_subword = word_to_subword
        self.subword_to_word = subword_to_word

        self.input_ids = input_ids
        self.input_mask = input_mask
        self.segment_ids = segment_ids

        self.seq = None
        self.sel_num = None
        self.sel = None
        self.agg = None
        self.where_num = None
        self.where = None
        self.op = None
        self.value_num = None
        self.value_start = None
        self.value_end = None
        self.relationship = None

        self.tokens_common = None

    def to_dict(self):
        return {
            'qid': self.qid,
            'question': self.question,
            'table_id': self.table_id,
            'tokens': self.tokens,
            'word_to_char_start': self.word_to_char_start,
            'word_to_subword': self.word_to_subword,
            'subword_to_word': self.subword_to_word,
            'input_ids': self.input_ids,
            'input_mask': self.input_mask,
            'segment_ids': self.segment_ids,

            'seq': self.seq,
            'sel_num': self.sel_num,
            'sel': self.sel,
            'agg': self.agg,
            'where_num': self.where_num,
            'where': self.where,
            'op': self.op,
            'value_num': self.value_num,
            'value_start': self.value_start,
            'value_end': self.value_end,
            'relationship': self.relationship
        }


class HydraColumnFeaturizer(object):
    """
        特征提取器，将一条训练数据集，转变成为InputFeature
    """

    def __init__(self, config, tokenizer):
        self.config = config
        # 根据不同模型，设置tokenizer
        self.tokenizer = tokenizer

    def get_predict_input_column_feature(self, example: SQLExample, schema: schema_parsed, config, note=True):
        """
            example 是一条完整的train数据
            example:
            {
                table_id,
                question,
                tokens,
                word_to_char_start,
                column_meta
                ...
                只用到这些
            }
            schema:
            {
                id,
                name,
                table_note,
                header,
                types,
                space,
                notes,
                feature  # 只用到feature
            }
            填充InputFeature其中的九个值
            InputFeature:
            {
                question,
                table_id,
                word_to_char_start,
                tokens,
                word_to_subword,
                subword_to_word,
                input_ids,
                input_mask,
                segment_ids
            }
        """
        max_query_length = int(config["max_query_length"])
        max_column_length = int(config["max_column_length"])
        max_total_length = max_column_length + max_query_length

        # 一条feature包含一条train,包含多个<>column<>question<>编码
        input_feature = ColumnInputFeature(
            example.qid,
            example.question,
            example.table_id,
            [],
            example.word_to_char_start,
            [],
            [],
            [],
            [],
            []
        )

        # 用于记录问题
        input_feature.tokens_common = example.tokens

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
            feature_type = 'feature_column'
        else:
            feature_type = 'feature_column_without_note'

        # 子加载与表对应的数据
        table = schema.extend_schema[example.table_id]
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

            # 0 1 划分方式
            # [cls] column [sep] question [sep]
            #   0     0      0      1       1
            # 获取column+[sep]的长度
            column_token_length = 0
            for i, sid in enumerate(segment_ids):
                if sid == 1:
                    column_token_length = i
                    break

            # 计算编码后的subword_to_word，需要加上column_token_length偏移
            subword_to_word = [0] * column_token_length + subword_to_word_base
            # 计算编码后的word_to_subword，需要加上column_token_length偏移
            word_to_subword = [(pos[0] + column_token_length, pos[1] + column_token_length) for pos in
                               word_to_subword_base]

            assert len(input_ids) == max_total_length
            assert len(input_mask) == max_total_length
            assert len(segment_ids) == max_total_length

            input_feature.tokens.append(new_tokens)
            input_feature.word_to_subword.append(word_to_subword)
            input_feature.subword_to_word.append(subword_to_word)
            input_feature.input_ids.append(input_ids)
            input_feature.input_mask.append(input_mask)
            input_feature.segment_ids.append(segment_ids)

        return input_feature

    def get_input_column_feature(self, example: SQLExample, schema: schema_parsed, config, positive=True, negative=True,
                                 note=False):
        """
            example 是一条完整的train数据
            example:
            {
                table_id,
                question,
                tokens,
                word_to_char_start,
                column_meta
                ...
                只用到这些
            }
            schema:
            {
                id,
                name,
                table_note,
                header,
                types,
                space,
                notes,
                feature  # 只用到feature
            }
            填充InputFeature其中的九个值
            InputFeature:
            {
                question,
                table_id,
                word_to_char_start,
                tokens,
                word_to_subword,
                subword_to_word,
                input_ids,
                input_mask,
                segment_ids
            }
        """
        max_query_length = int(config["max_query_length"])
        max_column_length = int(config["max_column_length"])
        max_total_length = max_column_length + max_query_length

        # 一条feature包含一条train,包含多个<>column<>question<>编码
        input_feature = ColumnInputFeature(
            example.qid,
            example.question,
            example.table_id,
            [],
            example.word_to_char_start,
            [],
            [],
            [],
            [],
            []
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
        rel_list = example.rel
        rel_table = example.table_id
        # 是否需要对输入进行拓展
        if note:
            feature_type = 'feature_column'
        else:
            feature_type = 'feature_column_without_note'

        for key, value in schema.extend_schema.items():
            # 只要正例
            if positive and not negative:
                if key != rel_table:
                    continue
            # 只要负例
            elif not positive and negative:
                if key == rel_table:
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

                # 0 1 划分方式
                # [cls] column [sep] question [sep]
                #   0     0      0      1       1
                # 获取column+[sep]的长度
                column_token_length = 0
                for i, sid in enumerate(segment_ids):
                    if sid == 1:
                        column_token_length = i
                        break

                # 计算编码后的subword_to_word，需要加上column_token_length偏移
                subword_to_word = [0] * column_token_length + subword_to_word_base
                # 计算编码后的word_to_subword，需要加上column_token_length偏移
                word_to_subword = [(pos[0] + column_token_length, pos[1] + column_token_length) for pos in
                                   word_to_subword_base]

                assert len(input_ids) == max_total_length
                assert len(input_mask) == max_total_length
                assert len(segment_ids) == max_total_length

                input_feature.tokens.append(new_tokens)
                input_feature.word_to_subword.append(word_to_subword)
                input_feature.subword_to_word.append(subword_to_word)
                input_feature.input_ids.append(input_ids)
                input_feature.input_mask.append(input_mask)
                input_feature.segment_ids.append(segment_ids)

        return input_feature

    # 填充特征
    def fill_label_column_feature_split(self, example: SQLExample, input_feature: ColumnInputFeature,
                                        schema: schema_parsed, config,
                                        positive=True, negative=True):
        """
            example:
            {
                qid,
                seq,
                agg,
                sel,
                conds,
                value_start_end
                relationship
            }
            input_feature:
            {
                tokens
                word_to_subword
                subword_to_word
                input_ids
                input_mask
                segment_ids
            }
        """
        max_query_length = int(config["max_query_length"])  # 最长query长度
        max_column_length = int(config["max_column_length"])  # 最长列长度
        max_total_length = max_column_length + max_query_length  # 最长序列长度

        # set relative column
        table_id = example.table_id
        # 只要正例
        if positive and not negative:
            global_sel_id = example.sel
            global_where_id = [cond[0] for cond in example.conds]
        # 只要负例
        elif not positive and negative:
            global_sel_id = []
            global_where_id = []
        # 正例和负例都要
        elif positive and negative:
            global_sel_id = [schema.local_to_global[str(table_id) + '/' + str(i)] for i in
                             example.sel]
            global_where_id = [schema.local_to_global[str(table_id) + '/' + str(cond[0])] for cond in
                               example.conds]
        else:
            assert False, 'Positive 和 Negative 不能全为负'

        # set column number
        col_num = len(input_feature.input_ids)  # 列数量

        # set seq
        input_feature.seq = [example.seq] * col_num
        # for i in global_sql_id:
        #     input_feature.seq[i] = example.seq

        # set sel_num
        input_feature.sel_num = [0] * col_num
        for i in global_sel_id:
            input_feature.sel_num[i] = len(example.sel)

        # input_feature.sel_num = [len(example.sel)] * col_num

        # set sel
        input_feature.sel = [0] * col_num
        for i in global_sel_id:
            input_feature.sel[i] = 1

        # set agg
        input_feature.agg = [0] * col_num
        for agg_index, global_col_index in enumerate(global_sel_id):
            input_feature.agg[global_col_index] = example.agg[agg_index]
        # for agg_index in range(0, len(example.sel)):
        #     local_id = example.sel[agg_index]
        #     global_id = schema.local_to_global[str(table_id) + '/' + str(local_id)]
        #     input_feature.agg[global_id] = example.agg[agg_index]

        # set where_num
        input_feature.where_num = [0] * col_num
        for i in global_where_id:
            input_feature.where_num[i] = len(example.conds)
        # input_feature.where_num = [len(example.conds)] * col_num

        # set relationship
        input_feature.relationship = [example.relationship] * col_num

        # init where op value_num
        input_feature.where = [0] * col_num
        input_feature.op = [0] * col_num
        input_feature.value_num = [0] * col_num

        # inti value_start_end
        input_feature.value_start = [[0] * int(config['max_value_num']) for i in range(0, col_num)]
        input_feature.value_end = [[0] * int(config['max_value_num']) for i in range(0, col_num)]

        # 只有正例需要
        if positive:
            # set where op value_num value_start_end
            for index, value in enumerate(example.conds):
                global_id = global_where_id[index]  # global id
                col_idx, op, value_num, value_span = value
                input_feature.where[global_id] = 1
                input_feature.op[global_id] = op
                input_feature.value_num[global_id] = value_num

                # 如果column没有对应的值，就跳过
                if len(value_span) == 0:
                    continue
                where_col_value_list = value_span
                # 遍历值
                for value_index, where_col_value in enumerate(where_col_value_list):
                    se = example.value_start_end[where_col_value]  # 获取value的value_start_end
                    try:
                        s = input_feature.word_to_subword[global_id][se[0]][0]  # 获取在编码过后的start_token
                        input_feature.value_start[global_id][value_index] = s
                        # -1 有可能导致大问题，后面看怎么用, 与span那里的l-1对应上了
                        # 这里-1 是预测的开始位置token，与word_to_subword和subword_to_word相对应
                        e = input_feature.word_to_subword[global_id][se[1]][1] - 1  # 获取在编码过后的end_token
                        input_feature.value_end[global_id][value_index] = e

                        # 断言，start_token 和 end_token 的位置均少于编码长度，并且对应input_mask位置的一个token
                        assert s < max_total_length and input_feature.input_mask[global_id][s] == 1
                        assert e < max_total_length and input_feature.input_mask[global_id][e] == 1
                    except:
                        print(example.qid, where_col_value)
                        print("value span is out of range")
                        return False
        return True

    # 加载数据
    def load_data(self, data_paths, config, schema, include_label=False, positive=True, negative=True, note=False):
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
            for k in ["seq", "sel_num", "sel", "agg", "where_num",
                      "where", "op", "value_num", "value_start", "value_end", "relationship"]:
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
                for example in SQLExample.load_from_json(line):
                    # 丢弃未经过验证并且包含sql_label的数据
                    if not example.valid and include_label == True:
                        continue

                    # 获取输入特征,返回一个对象，里面封装了多个<col,question>,<col,question>
                    input_feature = self.get_input_column_feature(example, schema, config, positive, negative, note)

                    # 如果包含sql_label, 则需要填充特征
                    if include_label:
                        success = self.fill_label_column_feature_split(example, input_feature, schema, config, positive,
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
                        model_inputs['seq'].extend(input_feature.seq)
                        model_inputs['sel_num'].extend(input_feature.sel_num)
                        model_inputs["sel"].extend(input_feature.sel)
                        model_inputs["agg"].extend(input_feature.agg)
                        model_inputs["where_num"].extend(input_feature.where_num)
                        model_inputs["where"].extend(input_feature.where)
                        model_inputs["op"].extend(input_feature.op)
                        model_inputs["value_num"].extend(input_feature.value_num)
                        model_inputs["value_start"].extend(input_feature.value_start)
                        model_inputs["value_end"].extend(input_feature.value_end)
                        model_inputs["relationship"].extend(input_feature.relationship)
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
    def load_predict_data(self, example: SQLExample, config, schema, note=True):
        # 将example,封装到model_input 中
        # 每一条数据是<>col<>question<>的特征
        model_inputs = {k: [] for k in ["input_ids", "input_mask", "segment_ids"]}
        # 记录输入每一个question所对应的特征序列
        pos = []
        # 多条<>column<>question<>特征
        input_features = []
        for table_id in example.first_schema_id + example.sec_schema_id:
            example.table_id = table_id
            # 获取输入特征,返回一个对象，里面封装了多个<col,question>,<col,question>
            input_feature = self.get_predict_input_column_feature(example, schema, config, note)

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


class ColumnDataset(torch_data.Dataset):
    def __init__(self, config, featurizer, schema):
        self.config = config
        self.featurizer = featurizer
        self.schema = schema
        self.input_features = None
        self.model_inputs = None
        self.pos = None

    def loads(self, data_paths, include_label=False, positive=True, negative=True, note=False):
        self.input_features, self.model_inputs, self.pos = self.featurizer.load_data(data_paths, self.config,
                                                                                     self.schema, include_label,
                                                                                     positive, negative, note)
        self.trans_data_type()
        print("file {0} loaded".format(data_paths))

    def load_for_predict(self, example: SQLExample, note=True):
        self.input_features, self.model_inputs, self.pos = self.featurizer.load_predict_data(example, self.config,
                                                                                             self.schema, note)
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
