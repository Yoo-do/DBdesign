import psycopg2
import DataClass

class PostgresLink:
    """
    连接PG
    """
    def __init__(self, host: str, database: str, port: str, user: str, password: str):
        self.host = host
        self.database = database
        self.port = port
        self.user = user
        self.password = password
        self.is_connected = False


    def connect_test(self):
        """
        测试连接
        :return:
        """
        try:
            self.conn = psycopg2.connect(host=self.host, database=self.database,
                                         port=self.port, user=self.user, password=self.password)
            self.conn.close()
            return True, 'ok'
        except Exception as e:
            return False, e.__str__()

    def get_connected(self):
        status, msg = self.connect_test()
        if status:
            self.conn = psycopg2.connect(host=self.host, database=self.database,
                                         port=self.port, user=self.user, password=self.password)
            self.is_connected = True


    def execute_sql(self, sql: str):
        if self.is_connected:
            self.cur = self.conn.cursor()
            self.cur.execute(sql)
            data = self.cur.fetchall()
            self.cur.close()

            return data

    def get_db_struct(self):
        """
        将数据库结构转换为标准结构
        :return:
        """
        db_struct = DataClass.DBStruct()
        schemas_list = self.get_all_schema_dict()

        # for schema_info in schemas_list:
        #     schema = DataClass.Schema(schema_info['schema_name'])
        #     table_list = self.get_table_list(schema_info['schema_id'])
        #     for table_info in table_list:
        #         column_list = self.get_column_list(schema_info['schema_name'], table_info['table_id'])



    def get_all_schema_list(self) -> [{}]:
        """
        获取全部的schema信息[{schema_id:str, schema_name:str}]
        :return:
        """
        if self.is_connected:
            schema_list = self.execute_sql(
            """
            with t as
            (select
                oid schema_id,
                nspname schema_name
                from pg_namespace
            where nspname not in ('pg_catalog', 'pg_toast'))
            select json_agg(row_to_json(t)) from t
            """)

            return schema_list[0][0]
    def get_table_list(self, schema_id: str) -> [{}]:
        """
        获取schema下全部的table信息[{table_id:str, table_name:str, table_note:str}]
        :param schema_id:
        :return:
        """
        if self.is_connected:
            table_list = self.execute_sql(
                f"""
                with t as(
                select
                oid table_id,
                relname table_name,
                (select description from pg_description where objoid = pc.oid and objsubid = 0) table_note
                from pg_class pc
                where relnamespace = {schema_id}
                and relkind = 'r')
                select json_agg(row_to_json(t)) from t
                """)

            return table_list[0][0]

    def get_column_list(self, schema_name:str, table_id:str, table_name:str) -> [{}]:
        """
        获取table下全部的column信息[{sort_no:str, column_name:str, chinese_name:str, data_type:str, allow_null:str}]
        :param schema_name:
        :param table_id:
        :param table_name:
        :return:
        """
        if self.is_connected:
            column_list = self.execute_sql(
                f"""
                with t as(
                select
                ordinal_position sort_no,
                column_name,
                (select description from pg_description where objoid = {table_id.__str__()} and objsubid = ordinal_position) chinese_name,
                case
                    when data_type in('character varying', 'character') then data_type::varchar||'('||character_maximum_length||')'
                    when data_type = 'numeric' then data_type::varchar||'('||numeric_precision||','||numeric_scale||')'
                    else data_type
                end data_type,
                case when is_nullable = 'NO' then '否' else '是' end allow_null
                from information_schema.columns
                where table_schema = '{schema_name}' and table_name = '{table_name}'
                order by ordinal_position)
                select json_agg(row_to_json(t)) from t
                """)

            return column_list[0][0]

    def close(self):
        if self.is_connected:
            self.conn.close()




def test1():
    link = PostgresLink('localhost', 'hdr', '5432', 'postgres', '123456')
    link.get_connected()
    print(link.get_all_schema_list())
    print(link.get_column_list('lab', 70142, 'lab_apply'))

if __name__ == '__main__':
    test1()