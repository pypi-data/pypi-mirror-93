import sys
from os.path import dirname, abspath

path = dirname(dirname(dirname(abspath(__file__))))
sys.path.append(path)
from Text2JSON.featurizer.column_featurizer import ColumnDataset, HydraColumnFeaturizer
from Text2JSON.featurizer.schema_featurizer import SchemaDataset, HydraSchemaFeaturizer


def load_train_column_data(config, schema, featurizer: HydraColumnFeaturizer, include_label=True, positive=True,
                           negative=True, note=False):
    train_data = ColumnDataset(config, featurizer, schema)
    train_data.loads(config["train_data_path"], include_label, positive, negative, note)
    return train_data


def load_eval_column_data(config, schema, featurizer: HydraColumnFeaturizer, include_label=True, positive=True,
                          negative=True, note=False):
    eval_path = config["dev_data_path"]
    data = ColumnDataset(config, featurizer, schema)
    data.loads(eval_path, include_label, positive, negative, note)
    print("Eval Data file {0} loaded".format(eval_path))
    return data


def load_train_schema_data(config, schema, featurizer: HydraSchemaFeaturizer, include_label=True, positive=True,
                           negative=True, note=False):
    train_schema_data = SchemaDataset(config, featurizer, schema)
    train_schema_data.loads(config["train_data_path"], include_label, positive, negative, note)
    print("Train Data file {0} loaded".format(config["train_data_path"]))
    return train_schema_data


def load_dev_schema_data(config, schema, featurizer: HydraSchemaFeaturizer, include_label=True, positive=True,
                         negative=True, note=False):
    # 这里需要重新加载
    eval_path = config["dev_data_path"]
    data = SchemaDataset(config, featurizer, schema)
    data.loads(eval_path, include_label, positive, negative, note)
    print("Dev Data file {0} loaded".format(config["dev_data_path"]))
    return data
