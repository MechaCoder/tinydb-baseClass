from unittest import TestCase
from random import choice

from tinydb.database import Document

from tinydb_base import DatabaseBase


class TestData(TestCase):

    def setUp(self):
        self.fileName = 'ds.test.json'
        return super().setUp()

    def testOne(self):
        """ tests creates """

        base = DatabaseBase(file=self.fileName)
        row = {
            'title': 'test'
        }

        self.assertIsInstance(
            base.create(row),
            int
        )

    def testTwo(self):
        """ test createMultiple"""

        base = DatabaseBase(file=self.fileName)

        rows = []
        for index in range(0, 75):
            row = {'title': f'x {index}'}
            rows.append(row)

        lisIds = base.createMultiple(rows)
        self.assertIsInstance(lisIds, list)
        for rowId in lisIds:
            self.assertIsInstance(
                rowId,
                int
            )

    def testThree(self):
        """ test read All """

        base = DatabaseBase(file=self.fileName)

        self.assertIsInstance(
            base.readAll(),
            list
        )

        for row in base.readAll():
            self.assertIsInstance(
                row,
                Document
            )

    def testFour(self):
        """ test read by id """
        base = DatabaseBase(file=self.fileName)
        base.create({'title': 'foobar'})
        randomRow = choice(base.readAll())
        row = base.readById(randomRow.doc_id)

        self.assertEqual(
            randomRow,
            row
        )

    def testFive(self):
        """ test remove by id """
        base = DatabaseBase(file=self.fileName)
        ident = base.create({'title': 'foobar'})
        row = base.removeById(ident)

        self.assertTrue(row)
