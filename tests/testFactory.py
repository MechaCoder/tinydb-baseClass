from unittest import TestCase

from tinydb import TinyDB
from tinydb.database import Table

from tinydb_base import Factory


class TestFactory(TestCase):

    def setUp(self):
        self.fileName = 'ds.test.json'
        return super().setUp()

    def test_one(self):
        """ i need to test weather db is present and is type checked """

        base = Factory(self.fileName, 'tbl')

        self.assertIsInstance(
            base.db,
            TinyDB
        )

        base.close()

    def test_two(self):
        """ i need to check weather the table is present and is type checked """
        base = Factory(self.fileName, 'tbl')

        self.assertIsInstance(
            base.tbl,
            Table
        )

        base.close()
