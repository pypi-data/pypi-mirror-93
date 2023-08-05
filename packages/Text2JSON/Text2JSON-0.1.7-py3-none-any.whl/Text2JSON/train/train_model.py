import sys
from os.path import dirname, abspath
path = dirname(dirname(dirname(abspath(__file__))))
sys.path.append(path)
import os
import datetime
import torch.utils.data as torch_data
from Text2JSON.train import utils
from Text2JSON.train.data_utils import *
from Text2JSON.evaluator.schema_evaluator import SchemaEvaluator
from Text2JSON.featurizer.schema_parser import schema_parsed
from Text2JSON.model.schema_model import HydraSchemaTorch
from Text2JSON.featurizer.schema_featurizer import HydraSchemaFeaturizer
from Text2JSON.evaluator.column_evaluator import ColumnEvaluator
from Text2JSON.model.column_model import HydraColumnTorch
from Text2JSON.predict.prediction import Predict


class ModelTrain(object):
    def __init__(self, conf_path, output_path, train_data_path, dev_data_path, schema_path, bert_path):
        """
            param: conf_path 配置文件路径
            param: output_path 模型输出路径
        """
        # 记载模型路径
        self.config = utils.read_conf(conf_path)
        # 训练数据存放位置
        self.config['train_data_path'] = train_data_path
        # 验证数据存放位置
        self.config['dev_data_path'] = dev_data_path
        # URL 处理后存放的路径
        self.config['schema_path'] = schema_path
        # 语言预训练模型存放位置
        self.config['bert_path'] = bert_path
        # 模型输出位置
        self.output_path = output_path
        # 加载tokenizer
        self.tokenizer = utils.create_tokenizer(self.config)
        # 加载数据表
        self.schema = schema_parsed()
        self.schema.load_schema(self.config, self.tokenizer)
        # 加载特征解析器
        self.schema_featurizer = HydraSchemaFeaturizer(self.config, self.tokenizer)
        # 加载特征解析器
        self.column_featurizer = HydraColumnFeaturizer(self.config, self.tokenizer)
        # 设置GPU还是CPU版本
        if 'CUDA_VISIBLE_DEVICES' in os.environ.keys():
            self.config['has_cuda'] = True
        else:
            self.config['has_cuda'] = False

    def train_column(self):
        # 记载训练数据，并将训练数据封装到dataloader中
        train_data = load_train_column_data(self.config, self.schema, self.column_featurizer, True, True, False,
                                            note=True)
        train_data_loader = torch_data.DataLoader(train_data,
                                                  batch_size=int(self.config["column_batch_size"]),
                                                  shuffle=True,
                                                  pin_memory=True)

        # negative train data
        negative_train_data = load_train_column_data(self.config, self.schema, self.column_featurizer, True, False,
                                                     True, note=True)
        negative_train_data_loader = torch_data.DataLoader(negative_train_data,
                                                           batch_size=int(self.config["neg_column_train_batch_size"]),
                                                           shuffle=True,
                                                           pin_memory=True)
        # 加载验证数据， 分别是eval column, eval table
        eval_data = load_eval_column_data(self.config, self.schema, self.column_featurizer, True, True, negative=False,
                                          note=True)

        # 加载模型
        model = HydraColumnTorch(self.config)
        if self.config['has_cuda']:
            model.to_gpu()
        # 加载验证器
        evaluator = ColumnEvaluator(self.output_path, self.config, model, eval_data)
        # 设置训练步数
        num_samples = len(train_data)  # 训练样本总数量
        self.config["column_num_train_steps"] = int(
            num_samples * int(self.config["column_epochs"]) / int(self.config["column_batch_size"]))  # 设置训练步数
        print("total_steps: {0}, warm_up_steps: {1}".format(self.config["column_num_train_steps"],
                                                            self.config["column_num_warmup_steps"]))

        # 初始化参数和优化器
        model.init_optimizer()

        # 列训练
        loss_avg, step, epoch, best_overall, result_str = 0.0, 0, 0, -0.1, None
        print("Column training")
        while True:
            for batch_id, batch in enumerate(train_data_loader):
                cur_loss = model.train_on_batch(batch)
                for neg_batch_id, neg_batch in enumerate(negative_train_data_loader):
                    if neg_batch_id >= int(self.config["neg_column_train_epoch"]):
                        break
                    cur_loss += model.train_on_batch(neg_batch)
                loss_avg = (loss_avg * step + cur_loss) / (step + 1)
                step += 1
                if batch_id % 100 == 0:
                    currentDT = datetime.datetime.now()
                    print("[{3}] epoch {0}, batch {1}, column_batch_loss={2:.4f}".format(epoch, batch_id, cur_loss,
                                                                                         currentDT.strftime(
                                                                                             "%m-%d %H:%M:%S")))

            r_str, acc = evaluator.eval(epoch)
            if acc['overall'] > best_overall:
                model.save(self.output_path, 'column')
                best_overall = acc['overall']
                result_str = r_str
            epoch += 1
            if epoch >= int(self.config["column_epochs"]):
                break
        # 将最好结果写入
        evaluator.append('final result', result_str)
        # 删除模型
        model.to_cpu()
        del model

    def train_schema(self):
        # 加载正样本train table data
        train_schema_data = load_train_schema_data(self.config, self.schema, self.schema_featurizer, True, True,
                                                   negative=False, note=True)
        train_schema_data_loader = torch_data.DataLoader(train_schema_data,
                                                         batch_size=int(self.config["schema_batch_size"]),
                                                         shuffle=True,
                                                         pin_memory=True)
        # 加载负样本train table data
        negative_train_schema_data = load_train_schema_data(self.config, self.schema, self.schema_featurizer, True,
                                                            False, True, note=True)
        negative_train_schema_data_loader = torch_data.DataLoader(negative_train_schema_data,
                                                                  batch_size=int(
                                                                      self.config["neg_schema_train_batch_size"]),
                                                                  shuffle=True,
                                                                  pin_memory=True)
        # 加载验证数据， 分别是eval column
        eval_schema_data = load_dev_schema_data(self.config, self.schema, self.schema_featurizer, True, True, True,
                                                note=True)
        # 加载模型
        model = HydraSchemaTorch(self.config)
        if self.config['has_cuda']:
            model.to_gpu()
        # 加载验证器
        evaluator = SchemaEvaluator(self.output_path, self.config, model, eval_schema_data)

        num_samples = len(train_schema_data_loader)  # 训练样本总数量
        self.config["schema_num_train_steps"] = int(
            num_samples * int(self.config["schema_epochs"]) / int(self.config["schema_batch_size"]))  # 设置训练步数
        print("start training")
        print("total_steps: {0}, warm_up_steps: {1}".format(self.config["schema_num_train_steps"],
                                                            self.config["schema_num_warmup_steps"]))

        # 初始化参数和优化器
        model.init_optimizer()

        # 表训练
        loss_avg, step, epoch, best_overall, result_str = 0.0, 0, 0, -0.1, None
        print("Schema training")
        while True:
            for batch_id, batch in enumerate(train_schema_data_loader):
                cur_loss = model.train_on_batch(batch)
                for neg_batch_id, neg_batch in enumerate(negative_train_schema_data_loader):
                    if neg_batch_id >= int(self.config["neg_schema_train_epochs"]):
                        break
                    cur_loss += model.train_on_batch(neg_batch)
                    loss_avg = (loss_avg * step + cur_loss) / (step + 1)
                if batch_id % 10 == 0:
                    currentDT = datetime.datetime.now()
                    print("[{3}] epoch {0}, batch {1}, table_batch_loss={2:.4f}".format(epoch, batch_id, cur_loss,
                                                                                        currentDT.strftime(
                                                                                            "%m-%d %H:%M:%S")))
            r_str, acc = evaluator.eval(epoch)
            if acc['overall'] > best_overall:
                model.save(self.output_path, 'schema')
                best_overall = acc['overall']
                result_str = r_str
            epoch += 1
            if epoch >= int(self.config["schema_epochs"]):
                break
        # 将最好结果写入
        evaluator.append('final result', result_str)
        # 删除模型
        model.to_cpu()
        del model

    def train(self):
        """
            function: 训练模型
        """
        self.train_schema()
        print('Schema Model train done')
        self.train_column()
        print('Column Model train done')

    def dump_client_model(self):
        """
            function: 导出客户端模型
        """
        schema_model = HydraSchemaTorch(self.config)
        schema_model.load(self.output_path, 'schema')
        column_model = HydraColumnTorch(self.config)
        column_model.load(self.output_path, 'column')
        predict = Predict()
        predict.set_params(self.config, self.tokenizer, self.schema_featurizer,
                           self.column_featurizer, self.schema, schema_model, column_model)
        predict.dump_model(os.path.join(self.output_path, "model.pt"))

        # 删除子模型
        os.remove(os.path.join(self.output_path, "model_schema.pt"))
        os.remove(os.path.join(self.output_path, "model_column.pt"))
