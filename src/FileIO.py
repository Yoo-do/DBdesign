import json
import os
import time

from DataClass import *
import base64
import xlwings
import path_lead

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
    def get_file_list() -> [str]:
        """
        获取resource文件夹下面的全部 db 后缀名文件
        :return:
        """
        # 只拿取.db后缀的文件
        file_paths = [x for x in os.listdir(path_lead.get_path(r'\resource')) if x.endswith('db')]
        files = [file_path.split('.')[0] for file_path in file_paths]

        return files
    @staticmethod
    def delete_db_file(file_name):
        file_path = os.path.join(path_lead.get_path(r'\resource'), file_name+'.db')
        os.remove(file_path)

    @staticmethod
    def get_db_struct(file_name):
        """
        通过文件名获取DBStruct
        :param file_name:
        :return:
        """
        file_path = os.path.join(path_lead.get_path(r'\resource'), file_name + '.db')
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
        file_path = os.path.join(path_lead.get_path(r'\resource'), file_name + '.db')
        FileIOUtil.write_encryption_data(file_path, json.dumps(db_struct.__json__()))

    @staticmethod
    def export_excel(data: DBStruct, file_path: str):
        begin_time = time.time()
        data.schemas.reverse()

        print(f'目标路径为{file_path}')
        with xlwings.App(visible=False, add_book=False) as app:
            link_path = []
            app.screen_updating = False
            book = app.books.add()
            for schema in data.schemas:
                print(f'正在写入{schema.schema_name}...')
                sheet = book.sheets.add(schema.schema_name)
                schema_links = {"schema_name": schema.schema_name, "schema_link": f'#{schema.schema_name}!A1', 'table_links': []}
                current_row = 1
                if len(schema.tables) == 0:
                    continue
                for table in schema.tables:
                    sheet.range(f'A{current_row}').value = table.table_name
                    table_name_cell = sheet.range(f'A{current_row}:E{current_row}')
                    table_name_cell.api.Merge()
                    table_name_cell.color = (255, 255, 0)
                    table_name_cell.api.HorizontalAlignment = -4108
                    table_name_cell.api.VerticalAlignment = -4108

                    schema_links['table_links'].append({'table_name': table.table_name, 'table_note': table.table_note, 'table_link': f'#{schema.schema_name}!A{current_row}'})

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

                link_path.append(schema_links)

            # 汇总sheet，并导入超链接
            current_row = 1
            sheet = book.sheets.add(f'{data.db_name}汇总')

            #标题设置
            sheet.range(f'A{current_row}').value = f'{data.db_name}汇总'
            tittle_cell = sheet.range(f'A{current_row}:B{current_row}')
            tittle_cell.api.Merge()
            tittle_cell.api.HorizontalAlignment = -4108
            tittle_cell.api.VerticalAlignment = -4108
            tittle_cell.color = (255, 255, 0)

            current_row += 1

            link_path.reverse()

            for sheet_link_item in link_path:
                sheet_start_row = current_row
                # schema 超链接设置
                sheet.range(f'A{sheet_start_row}').value = sheet_link_item['schema_name']
                sheet.range(f'A{sheet_start_row}').add_hyperlink(sheet_link_item['schema_link'], sheet_link_item['schema_name'], sheet_link_item['schema_name'])
                for table_link_item in sheet_link_item['table_links']:
                    sheet.range(f'B{current_row}').add_hyperlink(table_link_item['table_link'],
                                                                 table_link_item['table_name'] + (('(' + table_link_item['table_note'] + ')') if table_link_item['table_note'] is not None else ''),
                                                                 table_link_item['table_name'])
                    current_row += 1

                sheet.range(f'A{sheet_start_row}:A{current_row-1}').api.Merge()


            table_cell = sheet.range(f'A1:B{current_row - 1}')
            table_cell.api.HorizontalAlignment = -4108
            table_cell.api.VerticalAlignment = -4108
            table_cell.api.Borders.Weight = 2
            for col in table_cell.columns:
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


class DBConfigIO:
    class DBConfigInfo:
        def __init__(self, sort_no, link_name, host, database, port, user, password):
            self.sort_no = sort_no
            self.link_name = link_name
            self.host = host
            self.database = database
            self.port = port
            self.user = user
            self.password = password

        def __json__(self):
            js = {}
            js.update({'sort_no': self.sort_no})
            js.update({'link_name': self.link_name})
            js.update({'host': self.host})
            js.update({'database': self.database})
            js.update({'port': self.port})
            js.update({'user': self.user})
            js.update({'password': self.password})
            return js

    def __init__(self):
        self.config_path = path_lead.get_path(r'\config\dblink.ini')
        self.db_config: [DBConfigIO.DBConfigInfo] = []

        self.db_config_init()
    def db_config_init(self):
        """
        从固定路径获取数据库配置信息
        :return:
        """
        if not FileIOUtil.file_exists(self.config_path):
            FileIOUtil.write_file(self.config_path, [])

        db_config: list[dict] = FileIOUtil.read_file(self.config_path)
        for config in db_config:
            self.db_config.append(DBConfigIO.DBConfigInfo(config['sort_no'],
                                                          config['link_name'],
                                                          config['host'],
                                                          config['database'],
                                                          config['port'],
                                                          config['user'],
                                                          config['password']
                                                          ))

        self.db_config.sort(key=lambda x: int(x.sort_no))

    def get_link_names(self):
        return [config.link_name for config in self.db_config]

    def add_link(self, link_name):
        self.db_config.append(DBConfigIO.DBConfigInfo(f'{len(self.db_config)}', link_name, '', '', '5432', '', ''))

    def delete_link(self, sort_no):
        """
        删除对应序号的连接信息，删除后需要立即保存，并刷新数据
        :param sort_no:
        :return:
        """
        self.db_config.remove([config for config in self.db_config if config.sort_no == sort_no][0])

    def save_link(self):
        links = []
        self.db_config.sort(key=lambda x: int(x.sort_no))
        for sort_no, config in enumerate(self.db_config):
            config.sort_no = f'{sort_no}'
            links.append(config.__json__())

        FileIOUtil.write_file(self.config_path, links)




