import sys
from os.path import dirname, abspath

path = dirname(dirname(dirname(abspath(__file__))))
sys.path.append(path)
from Text2JSON.train import utils
from Text2JSON.predict.prediction import Predict
import datetime


def f_one(label_file, predict_file):
    stop_word_list = ['【', '】', '[', ']', '"', "'", '‘', '’', '“', '，', '.', '。', ' ', '”']
    label_data = utils.load_jsonl_by_key('qid', label_file)
    predit_data = utils.load_jsonl_by_key('qid', predict_file)
    sum_method_recall, sum_url_recall, sum_params_name_recall, \
    sum_params_op_recall, sum_params_value_recall, sum_rel_recall = 0., 0., 0., 0., 0., 0.

    sum_method_acc, sum_url_acc, sum_params_name_acc, \
    sum_params_op_acc, sum_params_value_acc, sum_rel_acc = 0., 0., 0., 0., 0., 0.

    for qid in label_data.keys():
        label = label_data[qid]
        predict = predit_data[qid]
        label_query = label['query']
        predict_query = predict['query']

        # predict parsing
        predict_params_name = {}
        predict_params_op = {}
        predict_params_value = {}
        for query in predict_query:
            url = query['url']
            name_to_option_dict = {}
            name_to_value_dict = {}
            predict_params_name[url] = []
            predict_params_op[url] = name_to_option_dict
            predict_params_value[url] = name_to_value_dict
            for params in query['params']:
                name = params['name']
                option = params['option']
                value = str(params['value'])
                for i in stop_word_list:
                    value = value.replace(i, '')
                value = value.split(',')
                predict_params_name[url].append(name)
                predict_params_op[url][name] = option
                predict_params_value[url][name] = value

        # label parsing
        label_params_name = {}
        label_params_op = {}
        label_params_value = {}
        for query in label_query:
            url = query['url']
            name_to_option_dict = {}
            name_to_value_dict = {}
            label_params_name[url] = []
            label_params_op[url] = name_to_option_dict
            label_params_value[url] = name_to_value_dict
            if 'params' not in query.keys():
                continue
            for params in query['params']:
                name = params['name']
                option = params['option']
                value = str(params['value'])
                for i in stop_word_list:
                    value = value.replace(i, '')
                value = value.split(',')
                label_params_name[url].append(name)
                label_params_op[url][name] = option
                label_params_value[url][name] = value

        rel_recall = 0.
        rel_acc = 0.
        # eval structure message
        if len(label_query) == len(predict_query):
            rel_acc = 1
            rel_recall = 1
        if len(label_query) > len(predict_query):
            rel_recall = (float(len(predict_query)) + 0.0001) / (len(label_query) + 0.0001)
            if len(predict_query) == 0:
                rel_acc = 0
            else:
                rel_acc = 1
        if len(predict_query) > len(label_query):
            rel_acc = (float(len(label_query)) + 0.0001) / (len(predict_query) + 0.0001)
            rel_recall = 1
        # eval url and method
        url_num = 0
        label_url = label_params_name.keys()
        predict_url = predict_params_name.keys()
        for url in label_url:
            if url in predict_url:
                url_num += 1

        url_acc = (url_num + 0.0001) / (float(len(predict_url)) + 0.0001)
        url_recall = (url_num + 0.0001) / (float(len(label_url)) + 0.0001)
        method_acc = url_acc
        method_recall = url_recall

        # eval params_name recall
        params_name_recall = 0
        for url, label_name_list in label_params_name.items():
            sub_name_num = 0
            if url not in predict_params_name.keys():
                continue
            predict_name_list = predict_params_name[url]

            for param in label_name_list:
                if param in predict_name_list:
                    sub_name_num += 1
            params_name_recall += (sub_name_num + 0.0001) / (float(len(label_name_list)) + 0.0001)
        params_name_recall = (params_name_recall + 0.0001) / (float(len(label_params_name.keys())) + 0.0001)

        # params acc
        params_name_acc = 0
        for url, predict_name_list in predict_params_name.items():
            sub_name_num = 0
            if url not in label_params_name.keys():
                continue
            label_name_list = label_params_name[url]
            for param in predict_name_list:
                if param in label_name_list:
                    sub_name_num += 1
            params_name_acc += (sub_name_num + 0.0001) / (float(len(predict_name_list)) + 0.0001)
        params_name_acc = (params_name_acc + 0.0001) / (float(len(predict_params_name.keys())) + 0.0001)

        # option recall
        params_op_recall = 0
        for url, label_option_dict in label_params_op.items():
            sub_op_num = 0
            if url not in predict_params_op.keys():
                continue
            predict_option_dict = predict_params_op[url]
            for key, op in label_option_dict.items():
                if key in predict_option_dict.keys():
                    if op == predict_option_dict[key]:
                        sub_op_num += 1
            params_op_recall += (sub_op_num + 0.0001) / (float(len(label_option_dict.keys())) + 0.0001)
        params_op_recall = (params_op_recall + 0.0001) / (float(len(label_params_op.keys())) + 0.0001)

        # option acc
        params_op_acc = 0
        for url, predict_option_dict in predict_params_op.items():
            sub_op_num = 0
            if url not in label_params_name.keys():
                continue
            label_option_dict = label_params_op[url]
            for key, op in predict_option_dict.items():
                if key in label_option_dict.keys():
                    if op == label_option_dict[key]:
                        sub_op_num += 1
            params_op_acc += (sub_op_num + 0.0001) / (float(len(predict_option_dict.keys())) + 0.0001)
        params_op_acc = (params_op_acc + 0.0001) / (float(len(predict_params_op.keys())) + 0.0001)

        # value recall
        params_value_recall = 0
        for url, label_value_dict in label_params_value.items():
            if url not in predict_params_value.keys():
                continue
            predict_value_dict = predict_params_value[url]
            sec_layer_recall = 0
            for key, value_list in label_value_dict.items():
                if key not in predict_value_dict:
                    continue
                value_num = 0
                for value in value_list:
                    if value in predict_value_dict[key]:
                        value_num += 1
                sec_layer_recall += (value_num + 0.0001) / (float(len(value_list) + 0.0001))
            params_value_recall += (sec_layer_recall + 0.0001) / (float(len(label_value_dict.keys()) + 0.0001))
        params_value_recall = (params_value_recall + 0.0001) / (float(len(label_params_value.keys()) + 0.0001))

        # value acc
        params_value_acc = 0
        for url, predict_value_dict in predict_params_value.items():
            if url not in label_params_value.keys():
                continue
            label_value_dict = label_params_value[url]
            sec_layer_acc = 0
            for key, value_list in predict_value_dict.items():
                if key not in label_value_dict:
                    continue
                value_num = 0
                for value in value_list:
                    if value in label_value_dict[key]:
                        value_num += 1
                sec_layer_acc += (value_num + 0.0001) / (float(len(value_list) + 0.0001))
            params_value_acc += (sec_layer_acc + 0.0001) / (float(len(predict_value_dict.keys()) + 0.0001))
        params_value_acc = (params_value_acc + 0.0001) / (float(len(predict_params_value.keys()) + 0.0001))

        sum_method_recall += method_recall
        sum_url_recall += url_recall
        sum_params_name_recall += params_name_recall
        sum_params_op_recall += params_op_recall
        sum_params_value_recall += params_value_recall
        sum_rel_recall += rel_recall

        sum_method_acc += method_acc
        sum_url_acc += url_acc
        sum_params_name_acc += params_name_acc
        sum_params_op_acc += params_op_acc
        sum_params_value_acc += params_value_acc
        sum_rel_acc += rel_acc

    cnt = len(label_data.keys())
    sum_method_recall = sum_method_recall / cnt
    sum_url_recall = sum_url_recall / cnt
    sum_params_name_recall = sum_params_name_recall / cnt
    sum_params_op_recall = sum_params_op_recall / cnt
    sum_params_value_recall = sum_params_value_recall / cnt
    sum_rel_recall = sum_rel_recall / cnt

    sum_method_acc = sum_method_acc / cnt
    sum_url_acc = sum_url_acc / cnt
    sum_params_name_acc = sum_params_name_acc / cnt
    sum_params_op_acc = sum_params_op_acc / cnt
    sum_params_value_acc = sum_params_value_acc / cnt
    sum_rel_acc = sum_rel_acc / cnt

    sum_recall = (sum_method_recall + sum_url_recall + sum_params_name_recall
                  + sum_params_op_recall + sum_params_value_recall + sum_rel_recall) / 6.

    sum_acc = (sum_method_acc + sum_url_acc + sum_params_name_acc + sum_params_op_acc
               + sum_params_value_acc + sum_rel_acc) / 6.

    f_one = (2 * sum_recall * sum_acc) / (sum_recall + sum_acc)
    result_str = 'F1:{0:.4f}, Recall:{1:.4f}, ACC:{2:.4f}'.format(f_one, sum_recall, sum_acc) + '\n' + \
                 '-------------------------------------------------------------------------------------' + '\n' + \
                 'Recall' + '\n' + \
                 'Method:{0:.4f}, URL:{1:.4f}, Name:{2:.4f}, Option:{3:.4f}, Value:{4:.4f}, Rel:{5:.4f}'. \
                     format(sum_url_recall, sum_url_recall, sum_params_name_recall, sum_params_op_recall,
                            sum_params_value_recall, sum_rel_recall) + '\n' + \
                 '-------------------------------------------------------------------------------------' + '\n' + \
                 'Accuracy' + '\n' + \
                 'Method:{0:.4f}, URL:{1:.4f}, Name:{2:.4f}, Option:{3:.4f}, Value:{4:.4f}, Rel:{5:.4f}'. \
                     format(sum_url_acc, sum_url_acc, sum_params_name_acc, sum_params_op_acc, sum_params_value_acc,
                            sum_rel_acc) + '\n'

    print('F1:{0:.4f}, Recall:{1:.4f}, ACC:{2:.4f}'.format(f_one, sum_recall, sum_acc))
    print('----------------------------------------------------------------------------------')
    print('Recall')
    print('Method:{0:.4f}, URL:{1:.4f}, Name:{2:.4f}, Option:{3:.4f}, Value:{4:.4f}, Rel:{5:.4f}'.format(sum_url_recall,
                                                                                                         sum_url_recall,
                                                                                                         sum_params_name_recall,
                                                                                                         sum_params_op_recall,
                                                                                                         sum_params_value_recall,
                                                                                                         sum_rel_recall))
    print('----------------------------------------------------------------------------------')
    print('Accuracy')
    print('Method:{0:.4f}, URL:{1:.4f}, Name:{2:.4f}, Option:{3:.4f}, Value:{4:.4f}, Rel:{5:.4f}'.
          format(sum_url_acc, sum_url_acc, sum_params_name_acc, sum_params_op_acc, sum_params_value_acc, sum_rel_acc))

    return result_str


def bleu_one(label_file, predict_file):
    stop_word_list = ['【', '】', '[', ']', '"', "'", '‘', '’', '“', '，', '.', '。', ' ', '”']
    label_data = utils.load_jsonl_by_key('qid', label_file)
    predit_data = utils.load_jsonl_by_key('qid', predict_file)
    sum_bleu = 0
    for qid in label_data.keys():
        label = label_data[qid]
        predict = predit_data[qid]
        label_query = label['query']
        predict_query = predict['query']

        # predict parsing
        predict_list = []
        for query in predict_query:
            url = query['url']
            method = query['method']
            predict_list.append(url)
            predict_list.append(method)
            for params in query['params']:
                name = params['name']
                option = params['option']
                value = str(params['value'])
                for i in stop_word_list:
                    value = value.replace(i, '')
                value = value.split(',')
                predict_list.append(name)
                predict_list.append(option)
                predict_list.extend(value)

        # label parsing
        label_list = []
        for query in label_query:
            url = query['url']
            method = query['method']
            label_list.append(url)
            label_list.append(method)
            if 'params' not in query.keys():
                continue
            for params in query['params']:
                name = params['name']
                option = params['option']
                value = str(params['value'])
                for i in stop_word_list:
                    value = value.replace(i, '')
                value = value.split(',')
                label_list.append(name)
                label_list.append(option)
                label_list.extend(value)

        bleu = 0
        for token in predict_list:
            if token in label_list:
                bleu += 1

        sum_bleu += float(bleu) / len(predict_list)

    sum_bleu = sum_bleu / len(predit_data.keys())
    result_str = 'BLEU-1:{0:.4f}'.format(sum_bleu) + \
                 '\n----------------------------------------------------------------------'
    print('BLEU-1:{0:.4f}'.format(sum_bleu))
    return result_str


def eval_bleu1_f1(model: Predict, label_path, output_path):
    """
        param: model 客户端模型
        label_path:
    """
    predict_list = []
    for data in utils.load_jsonl(label_path):
        qid = data['qid']
        question = data['question']
        predict_list.append(model.predict(question, qid=qid))

    utils.dump_jsonl(predict_list, output_path)
    a_result = bleu_one(label_path, output_path)
    b_result = f_one(label_path, output_path)
    return a_result, b_result
