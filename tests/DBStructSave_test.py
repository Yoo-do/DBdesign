import json

from src import FileIO


def test1():
    db_struct = FileIO.FileIOUtil.get_db_struct('hdr')

    FileIO.FileIOUtil.write_db_struct(db_struct, 'hdr2')


def test2():
    db_struct = FileIO.FileIOUtil.get_db_struct('hdr')
    db_json = db_struct.__json__()
    db_text = json.dumps(db_json)
    print(db_text)

if __name__ == '__main__':
    test1()
    # test2()