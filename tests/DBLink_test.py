from src import DBLink

def test1():
    db_link = DBLink.PostgresLink(host='localhost', database='oldhdr', port='5432', user='postgres', password='123456')
    db_link.get_connected()
    db_struct = db_link.get_db_struct('')
    print(db_struct)

def test2():
    db_link = DBLink.PostgresLink(host='localhost', database='oldhdr', port='5432', user='postgres', password='123456')
    db_link.get_connected()
    print(db_link.execute_sql('with t as (select * from lab.lab_report) select json_agg(row_to_json(t)) from t')[0][0])


if __name__ == '__main__':
    test1()