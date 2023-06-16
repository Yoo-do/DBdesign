class Column:
    def __init__(self, column_name, sort_no, chinese_name, column_type, allow_null):
        self.column_name = column_name
        self.sort_no = sort_no
        self.chinese_name = chinese_name
        self.column_type = column_type
        self.allow_null = allow_null


class Table:
    def __init__(self, table_name, table_note):
        self.table_name = table_name
        self.table_note = table_note
        self.columns: list[Column] = []

    def add_column(self, column: Column):
        self.columns.append(column)

    def column_sort(self):
        self.columns.sort(key=lambda x: x.sort_no, reverse=False)

    def get_column_infos(self):

        tittle_info = ['字段', '字段名', '类型', '允许空']
        result_info = []

        for column in self.columns:
            result_info.append(
                [column.column_name, column.chinese_name, column.column_type, column.allow_null])

        return tittle_info, result_info


class Schema:
    def __init__(self, schema_name):
        self.schema_name = schema_name
        self.tables: list[Table] = []

    def add_table(self, table: Table):
        self.tables.append(table)

    def get_table_num(self):
        return len(self.tables)

    def set_tables(self, tables: list[Table]):
        self.tables = tables

    def table_column_sort(self):
        for table in self.tables:
            table.column_sort()

    def get_table_names(self):
        return [table.table_name for table in self.tables]

    def get_table_notes(self):
        return [table.table_note for table in self.tables]

    def get_table(self, table_name):
        return [table for table in self.tables if table.table_name == table_name][0]

class DBStruct:
    def __init__(self, db_name):
        self.db_name = db_name
        self.schemas: list[Schema] = []

    def add_schema(self, schema: Schema):
        self.schemas.append(schema)

    def set_schemas(self, schemas: list[Schema]):
        self.schemas = schemas

    def get_schema_num(self):
        return len(self.schemas)

    def get_schema_names(self):
        return [schema.schema_name for schema in self.schemas]

    def get_schema(self, schema_name):
        return [schema for schema in self.schemas if schema.schema_name == schema_name][0]
