import os
import json
import transformers
import pickle


def load_jsonl(jsonl):
    for line in open(jsonl, encoding="utf8"):
        sample = json.loads(line.rstrip())
        yield sample


def dump_jsonl(data, path):
    with open(path, 'w', encoding='utf-8') as file_obj:
        for line in data:
            file_obj.writelines(json.dumps(line, ensure_ascii=False) + '\n')


def load_jsonl_by_key(key, filepath):
    table_dict = {}
    with open(filepath, 'r', encoding='utf8')as fp:
        for line in fp:
            line_json = json.loads(line)
            table_dict[line_json[key]] = line_json
        return table_dict


def load_json(filepath):
    with open(filepath, 'r', encoding='utf8')as fp:
        return json.load(fp)


def dump_json(data, filepath):
    with open(filepath, 'w', encoding='utf-8') as file_obj:
        json.dump(data, file_obj, ensure_ascii=False)


def dump_model(model, path):
    with open(path, 'wb') as f:
        pickle.dump(model, f)


def load_model(path):
    with open(path, 'rb') as f:
        return pickle.load(f)


def dump_probablity(data, path):
    with open(path, 'w', encoding='utf-8') as file_obj:
        for qid, line in data.items():
            file_obj.writelines(str(qid) + ' ' + str(line) + '\n')


def read_vocab(path):
    result_list = []
    with open(path, 'r', encoding='utf8')as fp:
        for line in fp:
            result_list.append(line.rstrip())
    return result_list


def ranking_by_length(noun_list):
    vocab_map = {}
    result_list = []
    for noun in noun_list:
        if len(noun) not in vocab_map.keys():
            vocab_map[len(noun)] = [noun]
        else:
            vocab_map[len(noun)].append(noun)
    key_list = sorted(vocab_map.keys(), reverse=True)
    for key in key_list:
        result_list.extend(vocab_map[key])
    return result_list


def read_conf(conf_path):
    config = {}
    for line in open(conf_path, encoding="utf8"):
        line = line.strip()
        if line.strip() == "" or line[0] == "#":
            continue
        try:
            sharp_index = line.index('#')
        except:
            sharp_index = len(line)
        fields = line[:sharp_index].split(" ")
        config[fields[0]] = fields[1]
    return config


def create_base_model(config):
    try:
        return transformers.BertModel.from_pretrained(config['bert_path'])
    except Exception:
        raise Exception("base_path {0} not supported".format(config['bert_path']))


def create_tokenizer(config):
    try:
        return transformers.BertTokenizer.from_pretrained(config['bert_path'])
    except Exception:
        raise Exception("base_path {0} not supported".format(config['bert_path']))


if __name__ == '__main__':
    a_list = ['一审', '二审', '三审', '大疆科技有限公司', '北京慧点科技有限公司']
    print(ranking_by_length(a_list))
