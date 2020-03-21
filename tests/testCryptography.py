from unittest import TestCase
from os import urandom

from tinydb_base.cryptography import FernetFactory
from tinydb_base.cryptography import DatabaseBaseSercure


class TestFernetFactory(TestCase):

    def testEncrypt(self):
        obj = FernetFactory('password', 'salt')
        testMsg = 'this is a test'
        token = obj.encrypt(testMsg)

        self.assertNotEqual(
            token,
            testMsg
        )

        self.assertIsInstance(
            token,
            str
        )

    def testDecrypt(self):
        obj = FernetFactory('password', 'salt')
        testMsg = 'this is a test'
        token = obj.encrypt(testMsg)
        newMsg = obj.decrypt(token)

        self.assertEqual(
            newMsg,
            testMsg
        )

        self.assertIsInstance(
            newMsg,
            str
        )


class TestDatabaseBaseSercure(TestCase):

    def setUp(self):
        self.salt = urandom(16)
        return super().setUp()

    def testCreate(self):

        obj = DatabaseBaseSercure('ds.test.json')
        rowId = obj.create({'title': 'foobar'}, 'pw')

        self.assertIsInstance(
            rowId,
            int
        )

    def testCreateMultiple(self):

        obj = DatabaseBaseSercure('ds.test.json')
        newIds = obj.createMultiple([{'title': 'test'}], 'pw')

        self.assertIsInstance(
            newIds,
            list
        )

        for e in newIds:

            self.assertIsInstance(
                e,
                int
            )

    def testReadAll(self):

        obj = DatabaseBaseSercure('ds.test.json')
        rows = obj.readAll('pw')

        self.assertIsInstance(rows, list)

        for e in rows:
            self.assertIsInstance(e, dict)

            self.assertIn(
                'title',
                e.keys()
            )

            self.assertIn('doc_id', e.keys())

        self.assertNotEqual(
            len(rows),
            0
        )

    def testReadById(self):

        obj = DatabaseBaseSercure('ds.test.json')
        row = obj.readById(1, 'pw')

        self.assertIsInstance(row, dict)
        self.assertIn('title', row.keys())
        self.assertIn('doc_id', row.keys())
