import sys
from os.path import dirname, abspath
path = dirname(dirname(dirname(abspath(__file__))))
sys.path.append(path)
import os
import numpy as np
from Text2JSON.featurizer.schema_featurizer import SchemaDataset
from Text2JSON.model.base_model import BaseModel


class SchemaEvaluator:
    def __init__(self, output_path, config, model: BaseModel, eval_schema_data):
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
        self.eval_history_file = os.path.join(output_path, "schema_eval.log")  # 预测结果存放位置
        f = open(self.eval_history_file, 'w')
        f.close()
        self.eval_schema_data = eval_schema_data

    # 改变这里的评测方式
    def eval_schema(self, eval_table_data: SchemaDataset):
        items = ['overall', 'first', 'first_contain']
        acc = {k: 0.0 for k in items}
        cnt = 0
        model_outputs = self.model.dataset_inference(eval_table_data)
        for input_feature, model_output in zip(eval_table_data.input_features, model_outputs):
            cur_acc = {'first': 1, 'first_contain': 1}

            schema_rel_label = input_feature.schema_rel

            if 1 not in input_feature.schema_mask:
                sql_seq = 1
            else:
                sql_seq = 2

            if sql_seq == 1:
                # parsing sql1 schema relevant
                schema_relevant_prob = np.exp(model_output['schema_first_sim'][:, 0])
                schema_id_prob_exp = sorted(enumerate(schema_relevant_prob), key=lambda x: x[1], reverse=True)
                schema_rel = []
                for table_index, table_pro in schema_id_prob_exp:
                    if table_pro >= float(self.config['schema_threshold']):
                        schema_rel.append(table_index)
                        if len(schema_rel) >= int(self.config['schema_remain']):
                            break
            else:
                # parsing sql2 schema relevant
                table_relevant_prob = np.exp(model_output['schema_sec_sim'][:, 0])
                table_id_prob_exp = sorted(enumerate(table_relevant_prob), key=lambda x: x[1], reverse=True)
                schema_rel = []
                for table_index, table_pro in table_id_prob_exp:
                    if table_pro >= float(self.config['schema_threshold']):
                        schema_rel.append(table_index)
                        if len(schema_rel) >= int(self.config['schema_remain']):
                            break

            # test schema relevant
            for index, value in enumerate(schema_rel_label):
                if value == 1 and (len(schema_rel) == 0 or index != schema_rel[0]):
                    cur_acc['first'] = 0
                if value == 1 and index not in schema_rel:
                    cur_acc['first_contain'] = 0
                    break

            # add all
            for k in cur_acc:
                acc[k] += cur_acc[k]

            all_correct = 0 if 0 in cur_acc.values() else 1
            cur_acc['overall'] = all_correct
            acc["overall"] += all_correct

            cnt += 1

        # set result
        result_str = []
        for item in items:
            result_str.append(item + ":{0:.1f}".format(acc[item] * 100.0 / cnt))
        result_str = ", ".join(result_str)
        return result_str, acc

    def eval(self, epochs):
        print('schema eval_file', self.config['dev_data_path'])
        result_str, acc = self.eval_schema(self.eval_schema_data)
        print("[ epochs " + str(epochs) + " ] " + result_str)
        with open(self.eval_history_file, "a+", encoding="utf8") as f:
            f.write("[{0}, epoch {1}] ".format(self.config['dev_data_path'], epochs) + result_str + "\n")
        return result_str, acc

    # 将最好结果写入
    def append(self, state, result_str):
        with open(self.eval_history_file, "a+", encoding="utf8") as f:
            f.write("[{0}, {1}] ".format(self.config['dev_data_path'], state) + result_str + "\n")




