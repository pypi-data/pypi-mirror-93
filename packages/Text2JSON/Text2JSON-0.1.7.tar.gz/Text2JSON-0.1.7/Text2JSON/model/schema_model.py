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


class HydraSchemaTorch(BaseModel):
    def __init__(self, config):
        # 配置文件config
        self.config = config
        # 根据config设置，加载对应的HydraNet
        self.schema_model = HydraSchemaNet(config)
        # 定义优化器，学习率优化器
        self.optimizer, self.scheduler = None, None

    def init_optimizer(self):
        # 衰退设定
        no_decay = ["bias", "LayerNorm.weight"]
        # 返回model的所有参数的(name, tensor)的键值对, 并且设置其值
        optimizer_grouped_parameters = [
            {
                "params": [p for n, p in self.schema_model.named_parameters() if not any(nd in n for nd in no_decay)],
                "weight_decay": float(self.config["decay"]),
            },
            {"params": [p for n, p in self.schema_model.named_parameters() if any(nd in n for nd in no_decay)],
             "weight_decay": 0.0},
        ]
        # AdamW是实现了权重衰减的优化器
        self.optimizer = transformers.AdamW(optimizer_grouped_parameters,
                                            lr=float(self.config["schema_learning_rate"]))
        # 设置耐心系数
        self.scheduler = transformers.get_cosine_schedule_with_warmup(
            self.optimizer,
            num_warmup_steps=int(self.config["schema_num_warmup_steps"]),
            num_training_steps=int(self.config["schema_num_train_steps"]))

        # 梯度清零
        self.optimizer.zero_grad()

    def train_on_batch(self, batch):
        self.schema_model.train()
        # 加载数据到cuda
        if self.config['has_cuda']:
            for k, v in batch.items():
                batch[k] = v.to(torch.device("cuda:0"))

        # 默认调用model.forward函数
        batch_loss = torch.mean(self.schema_model(**batch)["loss"])  # 计算loss

        batch_loss.backward()  # loss反向传播
        torch.nn.utils.clip_grad_norm_(self.schema_model.parameters(), 1.0)  # 用L2范数作为正则
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
        self.schema_model.eval()
        model_outputs = {}

        # batch_size = 512  # 设置步长， 这一步有可能出现内存溢出，内存太大了
        batch_size = int(self.config['schema_evaluator_batch_size'])
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

            # 因为只做预测，所以不更新梯度
            with torch.no_grad():
                # 数据输入模型
                model_output = self.schema_model(**input_tensor)

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

        # 写一下注释
        return model_outputs

    def save(self, model_path, name):
        save_path = os.path.join(model_path, "model_{0}.pt".format(name))
        torch.save(self.schema_model.state_dict(), save_path)
        print("Schema Model saved in path: %s" % save_path)

    def load(self, model_path, name):
        pt_path = os.path.join(model_path, "model_{0}.pt".format(name))
        self.schema_model.load_state_dict(torch.load(pt_path))
        print("Schema Model loaded from {0}".format(pt_path))

    def to_cpu(self):
        self.schema_model.cpu()

    def to_gpu(self):
        self.schema_model.to(torch.device("cuda:0"))


class HydraSchemaNet(nn.Module):
    def __init__(self, config):
        super(HydraSchemaNet, self).__init__()
        self.config = config

        # load bert model
        self.base_model = utils.create_base_model(config)

        drop_rate = float(config["drop_rate"]) if "drop_rate" in config else 0.0
        self.dropout = nn.Dropout(drop_rate)

        bert_hid_size = self.base_model.config.hidden_size  # 获取隐变量维度

        # 计算SQL1 的 table 相似度
        self.schema_first_sim = nn.Linear(bert_hid_size, 2)
        # 计算SQL2 的 table 相似度
        self.schema_sec_sim = nn.Linear(bert_hid_size, 2)

    def forward(self, input_ids, input_mask, segment_ids, schema_rel=None, schema_mask=None):
        # print('table_rel', table_rel)
        # print('table_seq', table_seq)
        # print('table_mask', table_mask)
        # 获取输出
        # bert_output 是最后一层编码层的特征向量 <cls>h,h,...,h<sep>q,q,...,q<sep>
        # pooled_output 是 cls
        _, pooled_output = self.base_model(
            input_ids=input_ids,
            attention_mask=input_mask,
            token_type_ids=segment_ids)

        # dropout 放弃部分值
        pooled_output = self.dropout(pooled_output)

        # schema simi
        schema_first_logit = self.schema_first_sim(pooled_output)
        schema_sec_logit = self.schema_sec_sim(pooled_output)

        loss = None
        # Not None 对应train的情况
        # None 对应inference的情况
        if schema_rel is not None:
            schema_rel = schema_rel.type_as(schema_first_logit)
            bceloss = nn.BCEWithLogitsLoss(reduction="none")  # 将sigmod函数和Binary CrossEntropyLoss合成一步

            # 计算table similarity loss
            loss = bceloss(schema_first_logit[:, 0], schema_rel) * (1 - schema_mask)
            loss += bceloss(schema_sec_logit[:, 0], schema_rel) * schema_mask

        log_sigmoid = nn.LogSigmoid()
        return {"schema_first_sim": log_sigmoid(schema_first_logit),
                'schema_sec_sim': log_sigmoid(schema_sec_logit),
                "loss": loss}
