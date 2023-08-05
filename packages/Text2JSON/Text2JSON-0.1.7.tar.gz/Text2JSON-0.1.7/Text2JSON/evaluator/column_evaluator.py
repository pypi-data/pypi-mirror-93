import sys
from os.path import dirname, abspath
path = dirname(dirname(dirname(abspath(__file__))))
sys.path.append(path)
import os
from Text2JSON.featurizer.column_featurizer import ColumnDataset
from Text2JSON.model.base_model import BaseModel


class ColumnEvaluator:
    def __init__(self, output_path, config, model: BaseModel, eval_data):
        """
            评估网络效果
            output_path: 结果输出路径
            config: 参数配置
            eval_data: 需要验证的数据
            hydra_featurizer: 特征提取器
            model: 模型
            note: 注释
        """
        self.config = config
        self.model = model
        self.eval_history_file = os.path.join(output_path, "column_eval.log")
        f = open(self.eval_history_file, 'w')
        f.close()
        # 预测结果存放位置
        self.eval_data = eval_data

    def eval_column(self, eval_data: ColumnDataset):
        # 10项评价指标
        items = ['overall', 'sc', 'agg', 'wc', 'op', 'vn', 'val', 'rel']

        # 建立映射
        acc = {k: 0.0 for k in items}
        cnt = 0
        '''
            每一个dict都是一条数据对应的多条<>column<>question<>的输出汇总
            model_outputs = [                
                {
                    'column_func': [[1,1,1], [1,1,1], ..., []]
                    'seq': [1, 1, 1, 0]
                    'sel': [[],[],...,[]]
                    'sel_num':[1, 1, 1, ..., 1]
                    'agg': [[], [],..., []] 
                    'where_num': [1, 1, 1, ..., 1]
                    'op': [[], [],..., []]
                    'value_num':[1, 1, 1, 1]
                    'value_start': [[], [], ..., []]
                    'value_end': [[], [], ..., []]
                    'relationship': [1, 1, 1, 1, 1]
                    'loss': [num1, num2, ..., ]
                },
                ...
            ]
        '''
        # 一次给整个数据集
        model_outputs = self.model.dataset_inference(eval_data)
        # input_features 作为label, model_outputs 作为predict
        for input_feature, model_output in zip(eval_data.input_features, model_outputs):
            # 设置当前验证数据的七项指标
            cur_acc = {k: 1 for k in acc.keys() if k != "overall"}

            sel_label = input_feature.sel
            agg_label = input_feature.agg
            wc_label = input_feature.where  # 获取where_clause对应的列
            op_label = input_feature.op
            value_num_label = input_feature.value_num
            value_start_end_label = []
            for index, value in enumerate(input_feature.where):
                if value == 0:
                    continue
                value_num = input_feature.value_num[index]
                value_start_end_label.append([(input_feature.value_start[index][i],
                                               input_feature.value_end[index][i])
                                              for i in range(0, value_num)])
            relationship_label = input_feature.relationship
            '''
                输出：
                seq =  [0, 0, 0]
                relationship = [0, 0, 0]
                sel_num = 2
                sel = [col_index1, col_index2]
                agg = [col_agg1, col_agg2]
                where_num = 2
                where = [col_index1, col_index2]
                value_num = [0, 1]
                conditions = {
                                col_index1:(col_index1, op_index1, [(s1, e1)])
                                col_index2:(col_index2, op_index2, [(s1, e1),(s2, e2)])
                            }
            '''
            # 选择解码方式
            # print('seq', input_feature.seq)
            if 1 not in input_feature.seq:
                sql_seq = 0
            else:
                sql_seq = 1

            sel, agg, where, value_num, conditions, relationship = \
                self.model.parse_output_with_threshold(input_feature, model_output, sql_seq,
                                                       float(self.config['column_threshold']))

            # relationship evaluate
            for pre_col_index, value in relationship:
                if int(relationship_label[pre_col_index]) != value:
                    cur_acc['rel'] = 0
                    break

            # (sel_col_index1, sel_col_index2)
            # (agg1, agg2)
            # sc evaluate
            for index, value in enumerate(sel_label):
                if value == 1 and index not in sel:
                    cur_acc['sc'] = 0
                    break

            # agg evaluate
            agg_dict = {}
            for index, value in agg:
                agg_dict[index] = value
            for index, value in enumerate(agg_label):
                if value == 0:
                    continue
                if index not in agg_dict.keys():
                    cur_acc['agg'] = 0
                    break
                if value != agg_dict[index]:
                    cur_acc['agg'] = 0
                    break

            # wc evaluate
            for index, value in enumerate(wc_label):
                if value == 1 and index not in where:
                    cur_acc['wc'] = 0
                    break

            # vn evaluate
            value_num_dict = {}
            for index, value in value_num:
                value_num_dict[index] = value

            for index, value in enumerate(value_num_label):
                if value == 0:
                    continue
                if index not in value_num_dict.keys():
                    cur_acc['vn'] = 0
                    break
                if value != value_num_dict[index]:
                    cur_acc['vn'] = 0
                    break

            for w in where:
                _, op, span_list = conditions[w]
                if op != op_label[w]:
                    cur_acc["op"] = 0

                for index, span in enumerate(span_list):
                    sv = span[0]
                    se = span[1]
                    if sv != input_feature.value_start[w][index] or \
                            se != input_feature.value_end[w][index]:
                        cur_acc["val"] = 0

            # 加到中的acc当中
            for k in cur_acc:
                acc[k] += cur_acc[k]

            # 计算overall
            all_correct = 0 if 0 in cur_acc.values() else 1
            cur_acc['overall'] = all_correct
            acc["overall"] += all_correct

            # 样本数自增1
            cnt += 1

        result_str = []
        for item in items:
            result_str.append(item + ":{0:.1f}".format(acc[item] * 100.0 / cnt))

        result_str = ", ".join(result_str)

        return result_str, acc

    def eval(self, epochs):
        print('column eval_file', self.config['dev_data_path'])
        result_str, acc = self.eval_column(self.eval_data)
        print("[ epochs " + str(epochs) + "] " + result_str)
        with open(self.eval_history_file, "a+", encoding="utf8") as f:
            f.write("[{0}, epoch {1}] ".format(self.config['dev_data_path'], epochs) + result_str + "\n")
        return result_str, acc

    # 将最好结果写入
    def append(self, state, result_str):
        with open(self.eval_history_file, "a+", encoding="utf8") as f:
            f.write("[{0}, {1}] ".format(self.config['dev_data_path'], state) + result_str + "\n")

