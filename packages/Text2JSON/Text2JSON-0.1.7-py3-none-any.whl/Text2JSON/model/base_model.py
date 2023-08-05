import numpy as np
import time


class BaseModel(object):
    """Define common interfaces for Hybrid Net models"""
    def to_cpu(self):
        raise NotImplementedError()

    def to_gpu(self):
        raise NotImplementedError()

    def train_on_batch(self, batch):
        raise NotImplementedError()

    def model_inference(self, model_inputs):
        """model prediction on processed features"""
        raise NotImplementedError()

    def save(self, model_path, name):
        raise NotImplementedError()

    def load(self, model_path, name):
        raise NotImplementedError()

    def dataset_inference(self, dataset):
        """model prediction on dataset"""
        print("model prediction start")
        start_time = time.time()
        # 获取预测输出
        model_outputs = self.model_inference(dataset.model_inputs)

        # 将输出按是否属于同一条数据进行分组
        # [{}, {}] 每一个dict都是一条数据对应的多条<>column<>question<>的输出汇总
        '''
            final_outputs = [                
                {
                    'column_func': [[1,1,1], [1,1,1], ..., []]
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
        # 分组打包
        final_outputs = self.data_packle(dataset, model_outputs)
        print("model prediction end, time elapse: {0}".format(time.time() - start_time))
        assert len(dataset.input_features) == len(final_outputs)

        return final_outputs

    # 将数据按是否属于同一个问题进行打包
    def data_packle(self, dataset, model_outputs):
        final_outputs = []
        for pos in dataset.pos:
            final_output = {}
            # 分组
            for k in model_outputs:
                final_output[k] = model_outputs[k][pos[0]:pos[1], :]
            final_outputs.append(final_output)
        return final_outputs

    def parse_output_with_threshold(self, input_feature, model_output, sql_seq=0, threshold=0.9):
        '''
            解析预测输出, agg, select, where, conditions
            model_output: 是以input_features数据作为输入，经过模型预测的输出
            input_feature: 数据的特征，可以认为是label
            sql_seq: SQL顺序，用哪一个解码器去进行解析
            threshold: 阈值

            一个条验证语句对应的所有<>column<>question<>作为输入，输出是其结果的集合
            假设一条验证数据一共有三条<>column<>question<>
            输出：
            sel_num = 2
            where_num = 2
            relationship = [0, 0, 0]
            sel = [col_index1, col_index2]
            agg = [(col_index1, col_agg1), (col_index2,col_agg2)]
            where = [col_index1, col_index2]
            value_num = [0, 1]
            conditions = {
                            col_index1:(col_index1, op_index1, [(s1, e1)])
                            col_index2:(col_index2, op_index2, [(s1, e1),(s2, e2)])
                        }
        '''

        # 根据seq，选择解析器，选择概率大于阈值的列
        if sql_seq == 0:
            sel_relevant_prob = np.exp(model_output["sql_first_select_sim"][:, 0])
            sel_id_prob_exp = sorted(enumerate(sel_relevant_prob), key=lambda x: x[1], reverse=True)
            sel = []
            for col_index, sel_col_pro in sel_id_prob_exp:
                if sel_col_pro >= threshold:
                    sel.append(col_index)

            where_relevant_prob = np.exp(model_output["sql_first_where_sim"][:, 0])
            where_id_prob_exp = sorted(enumerate(where_relevant_prob), key=lambda x: x[1], reverse=True)
            where = []
            for col_index, value in where_id_prob_exp:
                if value >= threshold:
                    where.append(col_index)

        else:
            sel_relevant_prob = np.exp(model_output["sql_sec_select_sim"][:, 0])
            sel_id_prob_exp = sorted(enumerate(sel_relevant_prob), key=lambda x: x[1], reverse=True)
            sel = []
            # 后续可以加入概率
            for col_index, sel_col_pro in sel_id_prob_exp:
                if sel_col_pro >= threshold:
                    sel.append(col_index)
            sel_num = len(sel)

            where_relevant_prob = np.exp(model_output["sql_sec_where_sim"][:, 0])
            where_id_prob_exp = sorted(enumerate(where_relevant_prob), key=lambda x: x[1], reverse=True)
            where = []
            for col_index, value in where_id_prob_exp:
                if value >= threshold:
                    where.append(col_index)
            where_num = len(where)

        # aggregation
        agg = [(index, np.argmax(model_output["agg"][index, :])) for index in sel]  # 选择该列对应的概率最高的集合操作符agg

        # value_num
        value_num = [(index, np.argmax(model_output["value_num"][index, :])) for index in where]

        # relationship
        relationship = [(index, np.argmax(model_output["relationship"][index, :])) for index in set(sel + where)]

        # 构建条件 conditions(col_id, op, value_span[0], value_span[1])
        conditions = {}
        for index in range(0, len(where)):
            where_col_idx = where[index]
            span_list = self.get_span(where_col_idx, value_num[index][1], input_feature, model_output)  # 获取span
            op = np.argmax(model_output["op"][where_col_idx, :])  # 获取与列对应概率最大的op
            conditions[where_col_idx] = (where_col_idx, op, span_list)  # 构造conditions

        return sel, agg, where, value_num, conditions, relationship

    def get_span(self, col_index, vn, input_feature, model_output):
        """
            function: 获取第i列对应个值
            输入：
                col_index: 列id
                vn: 列对应值得数量
                input_feature: 输入特征
                model_output: 输入特征经过模型处理后的输出
            输出：
                span_list = [(start1, end1), (start2, end2)]
        """
        offset = 0  # 记录
        segment_ids = np.array(input_feature.segment_ids[col_index])
        # 获取question token 开始位置
        for j in range(len(segment_ids)):
            if segment_ids[j] == 1:
                offset = j
                break

        # 获取question token位置的value_start 和 value_end 的概率， 一共max_value_num对start, end
        value_start = model_output["value_start"][col_index, segment_ids == 1]
        value_end = model_output["value_end"][col_index, segment_ids == 1]
        l = len(value_start)  # question token序列长度

        '''
            求对数空间下的start和end的联合概率矩阵 log(P(start, end))=logP(start)P(end)=logP(start)+logP(end)
            转变为shape 是 (l, l) 矩阵, 矩阵形式
                    i am here <SEP>
            i       1  1  1    1
            am      1  1  1    1
            here    1  1  1    1
            <SEP>   1  1  1    1
        '''
        # 默认第0个value_pointer 不用作计算
        span_list = []
        for index in range(1, vn + 1):
            sum_mat = value_start[:, index].reshape((l, 1)) + value_end[:, index].reshape((1, l))
            # 对矩阵中的每一个单元[(i,j),value]按value进行降序排序
            span = (0, 0)
            for cur_span, _ in sorted(np.ndenumerate(sum_mat), key=lambda x: x[1], reverse=True):
                # cur_span shape 是 (i, j), 因为已经进行了排序，所以value就不重要了
                # 一个假设，start<=end, 只有矩阵 上三角+对角线 才是合理的取值区间
                # or cur_span[0] == l - 1 or cur_span[1] == l - 1 l-1 是SEP，不取
                if cur_span[1] < cur_span[0]:
                    continue
                span = cur_span
                span_list.append((span[0] + offset, span[1] + offset))
                break
        return span_list
