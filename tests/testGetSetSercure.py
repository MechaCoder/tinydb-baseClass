from unittest import TestCase
from random import randint
from os import remove

from tinydb_base.getSetSercure import GetSetSercure
from tinydb_base.exceptions import RowNotFound_Exception


class TestGetSetSercure(TestCase):

    def setUp(self):
        self.fileName = 'ds.getsetSercure.test.json'
        self.salt = 'this is a salt'
        self.pw = 'this is a password'

    def test_set(self):
        obj = GetSetSercure(self.salt, self.pw, self.fileName)
        newId = obj.set('random_int', randint(0, 999))

        self.assertIsInstance(newId, bool)

    def test_get(self):
        obj = GetSetSercure(self.salt, self.pw, self.fileName)

        tag = "setings {}".format(randint(0, 999))
        val = randint(0, 100)

        obj.set(tag, val)

        v = obj.get(tag)

        self.assertIsInstance(v, str)
        self.assertEqual(str(val), v)

    def tearDown(self):
        # remove(self.fileName)
        return super().tearDown()
