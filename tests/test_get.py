import unittest

from pprint import pprint
from utilix import *


class TestGet(unittest.TestCase):

    def test_doc_by_number(self):
        db = rundb.DB()
        data = db.get_doc_by_number(2000)
        #pprint(data)
        self.assertTrue('data' in data)
        self.assertTrue('start' in data)
        self.assertTrue('source' in data)

    def test_doc_by_name(self):
        db = rundb.DB()
        data = db.get_doc_by_name('170917_1819')
        #pprint(data)
        self.assertTrue('data' in data)
        self.assertTrue('start' in data)
        self.assertTrue('source' in data)
    
    def test_data_by_number(self):
        db = rundb.DB()
        data = db.get_data_by_number(2000)
        #pprint(data)
        self.assertTrue('name' in data)
        self.assertTrue('number' in data)

    def test_data_by_name(self):
        db = rundb.DB()
        data = db.get_data_by_name('170917_1819')
        #pprint(data)
        self.assertTrue('name' in data)
        self.assertTrue('number' in data)

if __name__ == '__main__':
    unittest.main()

