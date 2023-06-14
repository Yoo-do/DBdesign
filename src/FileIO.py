import json
import os
from DataClass import *
import base64


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
            read_file(os.path.join('../resource/', file_name))
            files.append({'file_name': file_name, 'valid': True})
        except:
            files.append({'file_name': file_name, 'valid': True})

    return files


def read_file(file_path) -> [Schema]:
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
    print(get_file_list())
