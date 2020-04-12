from unittest import TestCase
from random import choice, random

from tinydb_base import DatabaseBase
from tinydb_base.output import exportToDict, exportToListOfDicts


class TestExport(TestCase):

    def testExportToDict(self):
        db = DatabaseBase('ds.test.json')

        for thing in range(0, 500):
            db.create({'title': '{}-{}'.format(thing, random())})

        randomRow = choice(db.readAll())

        obj = exportToDict(randomRow)

        self.assertIsInstance(
            obj,
            dict
        )

    def testExportToListOfDicts_Test(self):

        db = DatabaseBase('ds.test.json')
        rows = db.readAll()[0:25]

        converted = exportToListOfDicts(rows)
        self.assertIsInstance(converted, list)
        for row in converted:
            self.assertIsInstance(row, dict)
