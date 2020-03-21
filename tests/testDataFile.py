from unittest import TestCase

from tinydb import TinyDB


class TestDataFile(TestCase):

    def testOne(self):
        """ tests table names """
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
