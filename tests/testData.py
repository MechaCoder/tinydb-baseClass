from unittest import TestCase
from random import choice, randint
from os import remove

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

    def testOneA(self):
        base = DatabaseBase(self.fileName)

        with self.assertRaises(KeyError):
            base.create({'something': 0})

    def testSix(self):
        """ tests purgeing of a table """
        base = DatabaseBase(self.fileName, 'thing2')
        for e in range(0, randint(25, 50)):
            base.create({'title': 'foobar'})

        self.assertFalse(len(base.readAll()) == 0)
        base.clear()
        self.assertTrue(len(base.readAll()) == 0)

    def tearDown(self):
        try:
            remove(self.fileName)
        except:
            pass
        return super().tearDown()
