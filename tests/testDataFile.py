from unittest import TestCase
from os.path import exists

from tinydb import TinyDB


class TestDataFile(TestCase):

    def testOne(self):
        """ tests table names """

        if exists('ds.test.json') is False:
            self.skipTest()

        obj = TinyDB('ds.test.json')
        tableNames = obj.tables()
        obj.close()

        self.assertIn(
            'tinydb_base.data',
            tableNames
        )

        self.assertIn(
            'tinydb_base.cryptography',
            tableNames
        )

        self.assertIn(
            'tinydb_base.getSet',
            tableNames
        )
