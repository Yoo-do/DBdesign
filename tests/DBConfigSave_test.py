from src.FileIO import *

def test1():
    config_path = '../resource/dblink.ini'
    FileIOUtil.read_file(config_path)

if __name__ == '__main__':
    test1()