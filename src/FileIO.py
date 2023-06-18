import json
import os
from DataClass import *
import base64



class FileIOUtil:

    @staticmethod
    def file_exists(file_path) -> bool:
        """
        判断指定路径的文件是否存在
        :param file_path:
        :return:
        """
        return os.path.exists(file_path)

    @staticmethod
    def read_file(file_path) -> json:
        """
        读取指定路径文件并返回文件json内容
        :param file_path:
        :return: file_text
        """
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)

    @staticmethod
    def write_file(file_path, content: json):
        """
        将json内容写入文件
        :param file_path:
        :param content:
        :return:
        """
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(content, f)

    @staticmethod
    def get_db_config():
        """
        从固定路径获取数据库配置信息
        :return:
        """
        config_path = '../config/dblink.ini'
        if not FileIOUtil.file_exists(config_path):
            FileIOUtil.write_file(config_path, [])

        db_config: list[dict] = FileIOUtil.read_file(config_path)
        db_config.sort(key=lambda x: int(x['sort_no']))

        return db_config



class DBResourceFile:
    def __init__(self):
        pass



def get_file_list() -> [{str: bool}]:
    """
    获取resource文件夹下面的全部文件，并判断是否合法
    :return:
    """
    # 只拿取.db后缀的文件
    file_paths = [x for x in os.listdir('../resource') if x.endswith('db')]
    files = []

    for file_path in file_paths:
        file_name = file_path.split('.')[0]
        try:
            get_schemas_by_filepath(os.path.join('../resource/', file_path))
            files.append({'file_name': file_name, 'valid': True})
        except Exception as e:
            files.append({'file_name': file_name, 'valid': False})

    return files

def get_db_struct_by_file_name(file_name) -> DBStruct:
    db_struct = DBStruct(file_name)
    db_struct.set_schemas(get_schemas_by_filepath(os.path.join('../resource/', file_name + '.db')))
    return db_struct

def get_schemas_by_filepath(file_path) -> [Schema]:
    """
    解析指定数据库文件的内容，解析成Schema列表
    :return:
    """
    schemas = []

    schemas_dict: dict = json.loads(read_decryption_data(file_path))

    for schema_name, schema_val in schemas_dict.items():
        schema_obj = Schema(schema_name)
        for table in schema_val['tables']:
            table_obj = Table(table['table_name'], table['table_note'])
            for column in table['columns']:
                column_obj = Column(column_name=column['column_name'],
                                    sort_no=column['sort_no'],
                                    chinese_name=column['chinese_name'],
                                    column_type=column['column_type'],
                                    allow_null=column['allow_null'])
                table_obj.add_column(column_obj)
            table_obj.column_sort()
            schema_obj.add_table(table_obj)
        schemas.append(schema_obj)

    return schemas


def read_decryption_data(file_path) -> str:
    """
    读取目标文件内容并解密
    :param file_path: 目标文件路径
    :return:
    """
    with open(file_path, 'r') as f:
        return base64.b64decode(f.read().encode('utf-8')).decode('utf-8')


def write_encryption_data(file_path, text) -> str:
    """
    将内容加密写入目标路径中
    :param file_path:
    :param text:
    :return:
    """
    with open(file_path, 'w') as f:
        return base64.b64encode(text.encode('utf-8')).decode('utf-8')

if __name__ == '__main__':
    db_config = FileIOUtil.get_db_config()
    print(db_config)
    db_config.sort(key=lambda x: int(x['sort_no']))
    print(db_config)
