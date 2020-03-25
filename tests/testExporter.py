from unittest import TestCase
from os.path import exists 
from random import randint

from tinydb_base.exporter import jsonExport, ymalExport
from tinydb_base import DatabaseBase

class TestDB(DatabaseBase):

    def __init__(self, file='ds.test.json', table=__name__, requiredKeys=['title']):
        super().__init__(file=file, table=table, requiredKeys=requiredKeys)

class TestExporter(TestCase):

    def setUp(self):
        self.fileStamp = "data_{}".format(randint(1, 75))

        for title in range(0,90):
            TestDB().create({'title': title})
        
        self.data = TestDB().readAll()
        return super().setUp()

    def testJsonExport(self):

        o = jsonExport(
            self.data,
            self.fileStamp + '.json'
        )

        self.assertIsInstance(o, str)

    def testYmalExport(self):

        o = ymalExport(
            self.data,
            self.fileStamp + '.ymal'
        )

        self.assertIsInstance(o, str)