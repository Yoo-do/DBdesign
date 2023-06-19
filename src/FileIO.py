import json
import os
import time

from src.DataClass import *
import base64
import xlwings

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


    @staticmethod
    def get_file_list() -> [str]:
        """
        获取resource文件夹下面的全部 db 后缀名文件
        :return:
        """
        # 只拿取.db后缀的文件
        file_paths = [x for x in os.listdir('../resource') if x.endswith('db')]
        files = [file_path.split('.')[0] for file_path in file_paths]

        return files

    @staticmethod
    def get_db_struct(file_name):
        """
        通过文件名获取DBStruct
        :param file_name:
        :return:
        """
        file_path = os.path.join('../resource/', file_name + '.db')
        db_struct = DBStruct(file_name)

        schemas = []
        schemas_dict: dict = json.loads(FileIOUtil.read_decryption_data(file_path))

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

        db_struct.set_schemas(schemas)
        return db_struct

    @staticmethod
    def write_db_struct(db_struct: DBStruct, file_name: str):
        file_path = os.path.join('../resource/', file_name + '.db')
        FileIOUtil.write_encryption_data(file_path, json.dumps(db_struct.__json__()))

    @staticmethod
    def export_excel(data: DBStruct, file_path: str):
        begin_time = time.time()

        data.schemas.reverse()
        print(f'目标路径为{file_path}')
        with xlwings.App(visible=False, add_book=False) as app:
            app.screen_updating = False
            book = app.books.add()
            for schema in data.schemas:
                print(f'正在写入{schema.schema_name}...')
                sheet = book.sheets.add(schema.schema_name)
                current_row = 1
                for table in schema.tables:
                    sheet.range(f'A{current_row}').value = table.table_name
                    table_name_cell = sheet.range(f'A{current_row}:E{current_row}')
                    table_name_cell.api.Merge()
                    table_name_cell.color = (255, 255, 0)
                    table_name_cell.api.HorizontalAlignment = -4108
                    table_name_cell.api.VerticalAlignment = -4108
                    current_row += 1

                    sheet.range(f'A{current_row}').value = table.table_note
                    table_note_cell = sheet.range(f'A{current_row}:E{current_row}')
                    table_note_cell.api.Merge()
                    table_note_cell.color = (198, 224, 180)
                    table_note_cell.api.HorizontalAlignment = -4108
                    table_note_cell.api.VerticalAlignment = -4108
                    current_row += 1

                    sheet.range(f'A{current_row}:E{current_row}').value = (
                        '序号', '字段名', '中文名', '字段类型', '是否允许空')
                    current_row += 1

                    table.column_sort()
                    columns = []

                    for column in table.columns:
                        columns.append([column.sort_no, column.column_name, column.chinese_name, column.column_type,
                                        column.allow_null])

                    sheet.range(f'A{current_row}:E{current_row + len(columns) - 1}').value = (columns)
                    current_row += len(columns)

                sheet.range(f'A1:E{current_row - 1}').api.Borders.Weight = 2
                for col in sheet.range(f'A1:E{current_row - 1}').columns:
                    col.autofit()

            book.save(file_path)
            end_time = time.time()
            print(f'写入完毕, 共耗时{round(end_time-begin_time, 2)}s')

    @staticmethod
    def read_decryption_data(file_path) -> str:
        """
        读取目标文件内容并解密
        :param file_path: 目标文件路径
        :return:
        """
        with open(file_path, 'r') as f:
            return base64.b64decode(f.read().encode('utf-8')).decode('utf-8')

    @staticmethod
    def write_encryption_data(file_path, text) -> str:
        """
        将内容加密写入目标路径中
        :param file_path:
        :param text:
        :return:
        """
        with open(file_path, 'w') as f:
            f.write(base64.b64encode(text.encode('utf-8')).decode('utf-8'))


