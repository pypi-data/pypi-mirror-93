import sys
from os.path import dirname, abspath

path = dirname(dirname(dirname(abspath(__file__))))
sys.path.append(path)
import torch
import os
import numpy as np
import transformers
from Text2JSON.train import utils
from Text2JSON.model.base_model import BaseModel
from torch import nn


class HydraColumnTorch(BaseModel):
    def __init__(self, config):
        # 配置文件config
        self.config = config
        # 根据config设置，加载对应的HydraNet
        self.column_model = HydraColumnNet(config)
        # 定义优化器，学习率优化器
        self.optimizer, self.scheduler = None, None

    def init_optimizer(self):
        # 衰退设定
        no_decay = ["bias", "LayerNorm.weight"]
        # 返回model的所有参数的(name, tensor)的键值对, 并且设置其值
        optimizer_grouped_parameters = [
            {
                "params": [p for n, p in self.column_model.named_parameters() if not any(nd in n for nd in no_decay)],
                "weight_decay": float(self.config["decay"]),
            },
            {
                "params": [p for n, p in self.column_model.named_parameters() if any(nd in n for nd in no_decay)],
                "weight_decay": 0.0
            },
        ]
        # AdamW是实现了权重衰减的优化器
        self.optimizer = transformers.AdamW(optimizer_grouped_parameters,
                                            lr=float(self.config["column_learning_rate"]))
        # 设置耐心系数
        self.scheduler = transformers.get_cosine_schedule_with_warmup(
            self.optimizer,
            num_warmup_steps=int(self.config["column_num_warmup_steps"]),
            num_training_steps=int(self.config["column_num_train_steps"]))

        # 梯度清零
        self.optimizer.zero_grad()

    def train_on_batch(self, batch):
        self.column_model.train()
        # 加载数据到cuda
        if self.config['has_cuda']:
            for k, v in batch.items():
                batch[k] = v.to(torch.device("cuda:0"))

        # 默认调用model.forward函数
        batch_loss = torch.mean(self.column_model(**batch)["loss"])  # 计算loss

        batch_loss.backward()  # loss反向传播
        torch.nn.utils.clip_grad_norm_(self.column_model.parameters(), 1.0)  # 用L2范数作为正则
        self.optimizer.step()  # 优化
        self.scheduler.step()  # 更新学习率
        self.optimizer.zero_grad()  # 梯度清零

        if self.config['has_cuda']:
            # 返回一定需要detach, 否则会累积梯度
            return batch_loss.cpu().detach().numpy()
        else:
            return batch_loss.detach().numpy()

    # 模型预测
    def model_inference(self, model_inputs):
        # 不启用 BatchNormalization 和 Dropout
        self.column_model.eval()
        model_outputs = {}

        # batch_size = 512  # 设置步长， 这一步有可能出现内存溢出，内存太大了
        batch_size = int(self.config['column_evaluator_batch_size'])
        # 在(0~shape[0])之间遍历，步长为batch_size
        '''
            一个batch的输入格式
            input_tensor={
                            'input_ids': [],
                            'input_mask': [],
                            'segment_ids': []
                            }
        '''
        for start_idx in range(0, model_inputs["input_ids"].shape[0], batch_size):
            if self.config['has_cuda']:
                input_tensor = {
                    # 将batch中的数据分组，以batch_size为单位，分组
                    # 只取输入编码特征，不取其他特征
                    k: torch.from_numpy(model_inputs[k][start_idx:start_idx + batch_size]).to(torch.device("cuda:0"))
                    for k in ["input_ids", "input_mask", "segment_ids"]
                }
            else:
                input_tensor = {
                    # 将batch中的数据分组，以batch_size为单位，分组
                    # 只取输入编码特征，不取其他特征
                    k: torch.from_numpy(model_inputs[k][start_idx:start_idx + batch_size])
                    for k in ["input_ids", "input_mask", "segment_ids"]
                }
            '''
                一个batch输出格式
                model_output ={
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
                                }
            '''
            # 因为只做预测，所以不更新梯度
            with torch.no_grad():
                # 数据输入模型
                model_output = self.column_model(**input_tensor)

            # 将输出按关键字key进行分组
            for k, out_tensor in model_output.items():
                if out_tensor is None:
                    continue
                if k not in model_outputs:
                    model_outputs[k] = []
                if self.config['has_cuda']:
                    # 将数据转移到CPU，否则就会导致GPU内存溢出
                    model_outputs[k].append(out_tensor.cpu().detach().numpy())
                else:
                    model_outputs[k].append(out_tensor.detach().numpy())

        # 将多个batch结果合在一起
        for k in model_outputs:
            model_outputs[k] = np.concatenate(model_outputs[k], 0)

        '''
            concatenate前    [[[],[],...,[]], [[],[],...,[]]]
                                batch1          batch2
            concatenate后    [[],[],[],[],[],............[]]
            
            多个batch的最终输出
            model_outputs ={
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
                            }
        '''
        return model_outputs

    def save(self, model_path, name):
        save_path = os.path.join(model_path, "model_{0}.pt".format(name))
        torch.save(self.column_model.state_dict(), save_path)
        print("Column Model saved in path: %s" % save_path)

    def load(self, model_path, name):
        pt_path = os.path.join(model_path, "model_{0}.pt".format(name))
        self.column_model.load_state_dict(torch.load(pt_path))
        print("Column Model loaded from {0}".format(pt_path))

    def to_cpu(self):
        self.column_model.cpu()

    def to_gpu(self):
        self.column_model.to(torch.device("cuda:0"))


class HydraColumnNet(nn.Module):
    def __init__(self, config):
        super(HydraColumnNet, self).__init__()
        self.config = config

        # 加载transformer
        self.base_model = utils.create_base_model(config)

        drop_rate = float(config["drop_rate"]) if "drop_rate" in config else 0.0
        self.dropout = nn.Dropout(drop_rate)

        bert_hid_size = self.base_model.config.hidden_size  # 获取隐变量维度

        # 输入维度是bert_hid_size, 输出是3维, Loss用Sigmod+Binary CrossEntropyLoss函数计算
        # SQL1: 第一个是select相似度     p(c∈S|Q)  sel 中所选择的列
        # SQL1: 第二个是where相似度      p(c∈W|Q)  where 中所选择的列
        # SQL1: 第三个是整体相似度        p(c∈R|Q)  SQL 语句的整体相似度
        self.sql_first_select_sim = nn.Linear(bert_hid_size, 2)
        self.sql_first_where_sim = nn.Linear(bert_hid_size, 2)
        self.sql_first_all_sim = nn.Linear(bert_hid_size, 2)

        # SQL2: 第一个是select相似度     p(c∈S|Q)  sel 中所选择的列
        # SQL2: 第二个是where相似度      p(c∈W|Q)  where 中所选择的列
        # SQL2: 第三个是整体相似度        p(c∈R|Q)  SQL 语句的整体相似度
        # self.column_func_two = nn.Linear(bert_hid_size, 3)
        self.sql_sec_select_sim = nn.Linear(bert_hid_size, 2)
        self.sql_sec_where_sim = nn.Linear(bert_hid_size, 2)
        self.sql_sec_all_sim = nn.Linear(bert_hid_size, 2)

        # 计算输入的列操作符，loss=CrossEntropy
        self.agg = nn.Linear(bert_hid_size, int(config["agg_num"]))  # 输入维度是bert_hid_size, 输出是agg_num维
        # 计算输入的条件操作符，loss=CrossEntropy
        self.op = nn.Linear(bert_hid_size, int(config["op_num"]))  # 输入维度是bert_hid_size, 输出是op_num维

        # +1 是为了让0 作为没有值对应的value point， 第0维 不作训练
        # 用于计算输入在Where_Clause对应的值数目nv，p(nv|c,q)，loss=CrossEntropy
        self.value_num = nn.Linear(bert_hid_size, int(config["max_value_num"]) + 1)
        # 就上列对应值的 start_index, 一共可以对应max_value_num个值, Loss = CrossEntropy
        # [batch_size, token_num, hid_size] -> [batch_size, token_num, max_value_num]
        self.value_start = nn.Linear(bert_hid_size, int(config["max_value_num"]) + 1)
        # 就上列对应值的 end_index, 一共可以对应max_value_num个值, Loss = CrossEntropy
        # [batch_size, token_num, hid_size] -> [batch_size, token_num, max_value_num]
        self.value_end = nn.Linear(bert_hid_size, int(config["max_value_num"]) + 1)
        # 计算SQL语句之间的关系信息, loss = CrossEntropy
        self.relationship = nn.Linear(bert_hid_size, 2)

    def forward(self, input_ids, input_mask, segment_ids, seq=None, sel_num=None, sel=None, agg=None,
                where_num=None, where=None, op=None, value_num=None, value_start=None, value_end=None,
                relationship=None):
        """
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

        # 获取输出
        # bert_output 是最后一层编码层的特征向量 <cls>h,h,...,h<sep>q,q,...,q<sep>
        # pooled_output 是 cls
        bert_output, pooled_output = self.base_model(
            input_ids=input_ids,
            attention_mask=input_mask,
            token_type_ids=segment_ids)

        # dropout 放弃部分值
        bert_output = self.dropout(bert_output)
        pooled_output = self.dropout(pooled_output)

        # SQL 1
        sql_first_select_logit = self.sql_first_select_sim(pooled_output)
        sql_first_where_logit = self.sql_first_where_sim(pooled_output)
        sql_first_all_logit = self.sql_first_all_sim(pooled_output)

        # SQL 2
        sql_sec_select_logit = self.sql_sec_select_sim(pooled_output)
        sql_sec_where_logit = self.sql_sec_where_sim(pooled_output)
        sql_sec_all_logit = self.sql_sec_all_sim(pooled_output)

        # self.agg          :  [CLS] bert_hid_size -> config["agg_num"]
        # self.op           :  [CLS] bert_hid_size -> config["op_num"]
        # self.value_num    :  [CLS] bert_hid_size -> config["max_value_num"] + 1
        # self.value_start  :  [SEQ] bert_hid_size -> config["max_value_num"] + 1
        # self.value_end    :  [SEQ] bert_hid_size -> config["max_value_num"] + 1
        # self.relationship :  [CLS] bert_hid_size -> 2

        # public
        agg_logit = self.agg(pooled_output)
        op_logit = self.op(pooled_output)
        value_num_logit = self.value_num(pooled_output)  # 如果不行这里可以改一下
        value_start_logit = self.value_start(bert_output)
        value_end_logit = self.value_end(bert_output)
        relationship_logit = self.relationship(pooled_output)

        # 转换数据类型
        # 这里应该是用segment_ids, 因为start_index 和 end_index都不可能在column中，只能在question中
        value_span_mask = input_mask.to(dtype=bert_output.dtype)

        for index in range(0, int(self.config['max_value_num'])):
            value_start_logit[:, :, index + 1] = value_start_logit[:, :, index + 1] * value_span_mask - 1000000.0 * (
                    1 - value_span_mask)
            value_end_logit[:, :, index + 1] = value_end_logit[:, :, index + 1] * value_span_mask - 1000000.0 * (
                    1 - value_span_mask)

        loss = None
        # select is not None 对应train的情况
        # select is None 对应inference的情况
        if sel is not None:
            bceloss = nn.BCEWithLogitsLoss(reduction="none")  # 将sigmod函数和Binary CrossEntropyLoss合成一步
            cross_entropy = nn.CrossEntropyLoss(reduction="none")  # Cross Entropy Loss对应softmax函数的loss function

            select_rel = sel.float()
            where_rel = where.float()
            sql_rel = (sel.float() + where.float() - sel.float() * where.float())
            # SQL1 similarity loss
            loss = bceloss(sql_first_select_logit[:, 0], select_rel) * (1 - seq)
            loss += bceloss(sql_first_where_logit[:, 0], where_rel) * (1 - seq)
            loss += bceloss(sql_first_all_logit[:, 0], sql_rel) * (1 - seq)

            # SQL2 similarity loss
            loss += bceloss(sql_sec_select_logit[:, 0], select_rel) * seq
            loss += bceloss(sql_sec_where_logit[:, 0], where_rel) * seq
            loss += bceloss(sql_sec_all_logit[:, 0], sql_rel) * seq

            # SQL1 和 SQL2 可以共用的部分
            loss += cross_entropy(agg_logit, agg) * select_rel
            loss += cross_entropy(op_logit, op) * where_rel
            loss += cross_entropy(value_num_logit, value_num) * where_rel
            for index in range(0, int(self.config['max_value_num'])):
                loss += cross_entropy(value_start_logit[:, :, index + 1], value_start[:, index]) * where_rel
                loss += cross_entropy(value_end_logit[:, :, index + 1], value_end[:, index]) * where_rel
            loss += cross_entropy(relationship_logit, relationship) * sql_rel

        log_sigmoid = nn.LogSigmoid()
        return {"sql_first_select_sim": log_sigmoid(sql_first_select_logit),
                "sql_first_where_sim": log_sigmoid(sql_first_where_logit),
                "sql_first_all_sim": log_sigmoid(sql_first_all_logit),
                "sql_sec_select_sim": log_sigmoid(sql_sec_select_logit),
                "sql_sec_where_sim": log_sigmoid(sql_sec_where_logit),
                "sql_sec_all_sim": log_sigmoid(sql_sec_all_logit),
                "agg": agg_logit.log_softmax(1),
                "op": op_logit.log_softmax(1),
                "value_num": value_num_logit.log_softmax(1),
                "value_start": value_start_logit.log_softmax(1),
                "value_end": value_end_logit.log_softmax(1),
                "relationship": relationship_logit.log_softmax(1),
                "loss": loss}
