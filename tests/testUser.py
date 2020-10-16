from unittest import TestCase
from random import choices, random
from string import ascii_letters, punctuation, digits
from time import time

from tinydb_base.user import User


class TestUser(TestCase):

    def setUp(self):
        self.fileName = 'ds.user.test.json'
        return super().setUp()

    def tearDown(self):
        try:
            remove(self.fileName)
        except:
            pass
        return super().tearDown()

    def testOne(self):
        """ test makeUser """

        usr = User(self.fileName)
        uname = f'testuser{time()}'
        newUser = usr.makeUser(uname, 'password')
        self.assertIsInstance(newUser, int)

    def testTwo(self):
        """ test testUser """
        usr = User(self.fileName)

        uname = f'testuser{time()}'
        usr.makeUser(uname, 'password')

        self.assertTrue(
            usr.testUser(1, 'password')
        )
        self.assertFalse(
            usr.testUser(1, 'not the password')
        )

    def testThree(self):
        usr = User(self.fileName)
        pool = ascii_letters + digits + punctuation
        uname = ''.join(choices(pool, k=8))
        pword = ''.join(choices(pool, k=8))

        usr.makeUser(uname, pword)

        r = usr.authUser(uname, pword)
        self.assertTrue(r)
        self.assertFalse(usr.authUser(uname, pword + 'a'))
