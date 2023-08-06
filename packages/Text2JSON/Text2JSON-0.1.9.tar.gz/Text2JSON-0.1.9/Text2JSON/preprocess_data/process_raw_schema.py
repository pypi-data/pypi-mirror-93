import sys
from os.path import dirname, abspath
path = dirname(dirname(dirname(abspath(__file__))))
sys.path.append(path)
from Text2JSON.train import utils


class ProcessedSchema(object):
    def __init__(self):
        self.url_id = ''
        self.url = ''
        self.method = ''
        self.url_note = ''
        self.header = []
        self.types = []
        self.space = []
        self.notes = []

    def to_dict(self):
        return {
            "id": self.url_id,
            "url": self.url,
            "method": self.method,
            "url_note": self.url_note,
            "header": self.header,
            "types": self.types,
            "space": self.space,
            "notes": self.notes
        }


def gen_processed_schema(source, target):
    schema_list = []
    for data in utils.load_jsonl(source):
        schema = ProcessedSchema()
        schema.url_id = data['id']
        schema.url = data['url']
        schema.method = data['method']
        schema.url_note = data['url_note']
        schema.header = ["order&asc", "order&desc"]
        schema.types = ["string", "string"]
        schema.space = ["closed", "closed"]
        schema.notes = ["升序,最少,最小,最低", "降序,最大,最高"]
        params = data['params']
        for param in params:
            param_name = param['param_name']
            param_note = param['param_note']
            value_type = param['value_type']
            value_space = param['value_space']
            value_range = param['value_range']
            value_note = param['value_note']
            if param_name == 'order':
                continue
            if value_space == 'closed':
                for index, value in enumerate(value_range):
                    schema.header.append(param_name+'&'+value)
                    schema.types.append(value_type)
                    schema.space.append(value_space)
                    if param_note == '':
                        schema.notes.append(value_note[index])
                    else:
                        schema.notes.append(param_note+','+value_note[index])
            else:
                schema.header.append(param_name)
                schema.types.append(value_type)
                schema.space.append(value_space)
                schema.notes.append(param_note)
        schema_list.append(schema)
    schema_jsonl = [schema.to_dict() for schema in schema_list]
    utils.dump_jsonl(schema_jsonl, target)
