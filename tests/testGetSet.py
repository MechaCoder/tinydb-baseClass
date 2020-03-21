from unittest import TestCase
from random import randint

from tinydb_base.getSet import GetSet
from tinydb_base.exceptions import RowNotFound_Exception


class TestGetSet(TestCase):

    def setUp(self):
        self.fileName = 'ds.test.json'

    def test_set(self):
        obj = GetSet(self.fileName)
        newId = obj.set('random_int', randint(0, 999))

        self.assertIsInstance(newId, int)

    def test_get(self):
        obj = GetSet(self.fileName)

        tag = "setings {}".format(randint(0, 999))
        val = randint(0, 100)

        obj.set(tag, val)

        v = obj.get(tag)
        self.assertIsInstance(v, int)
        self.assertEqual(val, v)

    def test_get_one(self):
        obj = GetSet(self.fileName)

        with self.assertRaises(RowNotFound_Exception) as context:
            obj.get('setings 101')
