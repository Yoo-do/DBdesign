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