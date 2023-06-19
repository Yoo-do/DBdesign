import time

from src.FileIO import *

def test1():
    data = FileIOUtil.get_db_struct('hdr')
    data.schemas.reverse()
    with xlwings.App(visible=False, add_book=False) as app:
        app.screen_updating = False
        book = app.books.add()
        for schema in data.schemas:
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
                    columns.append([column.sort_no, column.column_name, column.chinese_name, column.column_type, column.allow_null])

                sheet.range(f'A{current_row}:E{current_row+len(columns)-1}').value = (columns)
                current_row += len(columns)

            sheet.range(f'A1:E{current_row - 1}').api.Borders.Weight = 2
            for col in sheet.range(f'A1:E{current_row - 1}').columns:
                col.autofit()

        book.save('../resource/test1.xlsx')

if __name__ == '__main__':
    begin_time = time.time()
    test1()
    end_time = time.time()
    print(end_time - begin_time)