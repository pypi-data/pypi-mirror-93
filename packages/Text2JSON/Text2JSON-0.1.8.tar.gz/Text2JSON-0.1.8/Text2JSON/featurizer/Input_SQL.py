import json


class SQLExample(object):
    def __init__(self):
        """
            这是拆分过后SQL
        """
        self.qid = None
        self.table_id = None
        self.table_id_relative = None
        self.question = None
        self.tokens = None
        self.char_to_word = None
        self.word_to_char_start = None

        self.seq = None
        self.agg = None
        self.sel = None
        self.conds = None
        self.rel = None
        self.value_start_end = None
        self.relationship = None
        self.valid = None

        # 预测时记载数据时用的
        self.first_schema_id = []
        self.sec_schema_id = []

    # 静态方法
    @staticmethod
    def load_from_json(s):
        data = json.loads(s)
        example_list = []
        qid = data['qid']
        question = data['question']
        tokens = data['tokens']
        char_to_word = data['char_to_word']
        word_to_char_start = data['word_to_char_start']
        valid = data['valid']
        for index in range(0, len(data['sql']['clause'])):
            table_id = data['table_id'][index]
            table_id_relative = data['table_id'][:index]+data['table_id'][index+1:]
            seq = data['sql']['clause'][index]['seq']
            sel = data['sql']['clause'][index]['sel']
            agg = data['sql']['clause'][index]['agg']
            conds = data['sql']['clause'][index]['conds']
            value_start_end = data['sql']['clause'][index]['value_start_end']
            relationship = data['sql']['relationship']

            rel = []
            rel.extend(sel)
            for cond in conds:
                rel.append(cond[0])

            example = SQLExample()
            example.qid = qid
            example.table_id = table_id
            example.table_id_relative = table_id_relative
            example.question = question
            example.tokens = tokens
            example.char_to_word = char_to_word
            example.word_to_char_start = word_to_char_start
            example.seq = seq
            example.sel = sel
            example.agg = agg
            example.conds = conds
            example.rel = rel
            example.value_start_end = value_start_end
            example.relationship = relationship
            example.valid = valid
            example_list.append(example)
        return example_list

if __name__ == "__main__":
    ''