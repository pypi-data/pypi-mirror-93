import sys
from os.path import dirname, abspath
path = dirname(dirname(dirname(abspath(__file__))))
sys.path.append(path)
from Text2JSON.train import utils
import re


class schema_parsed(object):
    def __init__(self):
        self.extend_schema = {}
        # 局部列序号到列全局序号的相互映射
        self.global_to_local = {}
        self.local_to_global = {}
        # 局部表序号到表全局序号的相互映射
        self.table_global_to_local = {}
        self.table_local_to_global = {}
        self.url_method = {}
        self.column_length = 0

    def load_schema(self, config, tokenizer):
        self.extend_schema = utils.load_jsonl_by_key('id', config['schema_path'])
        self.extend_schema_feature(tokenizer)
        self.extend_schema_feature_without_note(tokenizer)
        self.extend_schema_table_feature(tokenizer)
        self.extend_schema_table_feature_without_note(tokenizer)

        self.global_to_local, self.local_to_global = self.parse_column_map(self.extend_schema)
        self.table_global_to_local, self.table_local_to_global = self.parse_table_map(self.extend_schema)

        self.url_method = self.url_mathod_map(self.extend_schema)
        self.column_length = len(self.global_to_local.keys())

    def save_schema(self, config):
        utils.dump_model(self, config['featured_schema_path'])
        print('{0} file have been featured and the featured file saved in {1}'.
              format(config["schema_path"], config['featured_schema_path']))

    def parse_table_map(self, extend_schema):
        """
            local_global_map : table_id + col_id -> global_col_id 将局部col_id 映射到全局col_id
            global_local_map : global_col_id -> table_id + col_id 将全局col_id 映射到局部col_id
        """
        table_global_local_map = {}
        table_local_global_map = {}
        cur_id = 0
        for table_id, value in extend_schema.items():
            table_local_global_map[table_id] = cur_id
            table_global_local_map[cur_id] = table_id
            cur_id += 1
        return table_global_local_map, table_local_global_map

    def parse_column_map(self, extend_schema):
        """
            local_global_map : table_id + col_id -> global_col_id 将局部col_id 映射到全局col_id
            global_local_map : global_col_id -> table_id + col_id 将全局col_id 映射到局部col_id
        """
        global_local_map = {}
        local_global_map = {}
        cur_id = 0
        for table_id, value in extend_schema.items():
            for col_id in range(0, len(value['header'])):
                local_id = str(table_id)+"/"+str(col_id)
                local_global_map[local_id] = cur_id
                global_local_map[cur_id] = str(table_id)+"/"+str(col_id)
                cur_id += 1
        return global_local_map, local_global_map

    def extend_schema_feature_without_note(self, tokenizer):
        # extend feature
        # table_name table_note, column_name, column_type, column_note, column_space
        for key, value in self.extend_schema.items():
            feature_list = []
            table_name = value['url']
            # table_note = value['table_note']
            table_name_list = re.split('[/_]', table_name)
            # table_note_list = re.split('[,]', table_note)
            for index in range(0, len(value['header'])):
                sub_token = []
                column_name = value['header'][index]
                column_type = value['types'][index]
                # column_note = value['notes'][index]
                column_space = value['space'][index]

                column_name_list = re.split('[&_/]', column_name)
                column_type_list = re.split('[,]', column_type)
                # column_note_list = re.split('[,]', column_note)
                column_space_list = re.split('[,]', column_space)

                sub_token.extend(table_name_list)
                # sub_token.extend(table_note_list)
                sub_token.extend(column_name_list)
                sub_token.extend(column_type_list)
                # sub_token.extend(column_note_list)
                sub_token.extend(column_space_list)
                sequence = ' '.join(sub_token).strip()
                feature_list.append(tokenizer.tokenize(sequence))
            value['feature_column_without_note'] = feature_list

    def extend_schema_feature(self, tokenizer):
        # extend feature
        # table_name table_note, column_name, column_type, column_note, column_space
        for key, value in self.extend_schema.items():
            feature_list = []
            table_name = value['url']
            table_note = value['url_note']
            table_name_list = re.split('[/_]', table_name)
            table_note_list = re.split('[,]', table_note)
            for index in range(0, len(value['header'])):
                sub_token = []
                column_name = value['header'][index]
                column_type = value['types'][index]
                column_note = value['notes'][index]
                column_space = value['space'][index]

                column_name_list = re.split('[&_/]', column_name)
                column_type_list = re.split('[,]', column_type)
                column_note_list = re.split('[,]', column_note)
                column_space_list = re.split('[,]', column_space)

                sub_token.extend(table_name_list)
                sub_token.extend(table_note_list)
                sub_token.extend(column_name_list)
                sub_token.extend(column_type_list)
                sub_token.extend(column_note_list)
                sub_token.extend(column_space_list)
                sequence = ' '.join(sub_token).strip()
                feature_list.append(tokenizer.tokenize(sequence))
            value['feature_column'] = feature_list

    def extend_schema_table_feature(self, tokenizer):
        meanless_list = ['v2']
        # extend feature
        # table_name table_note, column_name, column_type, column_note, column_space
        for key, value in self.extend_schema.items():
            feature_list = []
            table_name = value['url']
            table_note = value['url_note']
            table_name_list = re.split('[/_]', table_name)
            for stop_word in meanless_list:
                if stop_word in table_name_list:
                    table_name_list.remove(stop_word)
            table_note_list = re.split('[,]', table_note)
            sub_token = []
            sub_token.extend(table_name_list)
            sub_token.extend(table_note_list)
            sequence = ' '.join(sub_token).strip()
            feature_list.append(tokenizer.tokenize(sequence))
            value['feature_schema'] = feature_list

    def extend_schema_table_feature_without_note(self, tokenizer):
        meanless_list = ['v2']
        # extend feature
        # table_name table_note, column_name, column_type, column_note, column_space
        for key, value in self.extend_schema.items():
            feature_list = []
            table_name = value['url']
            table_name_list = re.split('[/_]', table_name)
            for stop_word in meanless_list:
                if stop_word in table_name_list:
                    table_name_list.remove(stop_word)
            sub_token = []
            sub_token.extend(table_name_list)
            sequence = ' '.join(sub_token).strip()
            feature_list.append(tokenizer.tokenize(sequence))
            value['feature_schema_without_note'] = feature_list

    def url_mathod_map(self, extend_schema):
        url_method = {}
        for key in extend_schema:
            schema = extend_schema[key]
            url_method[schema['url']] = schema['method']
        return url_method

    def to_dict(self):
        return {
            'local_to_global': self.local_to_global,
            'global_to_global': self.global_to_local
        }
