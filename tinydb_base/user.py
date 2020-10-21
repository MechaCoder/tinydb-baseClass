from hashlib import pbkdf2_hmac
from os import urandom

from tinydb import Query

from .data import DatabaseBase
from .exceptions import UsernameExists


def mkpassword(passcode: str, salt: bytes) -> str:
    # salt = urandom(32)
    key = pbkdf2_hmac(
        'sha256',
        passcode.encode('utf-8'),
        salt,
        100000
    )

    return salt.hex() + key.hex()


class User(DatabaseBase):

    def __init__(self, file='ds.json', table='users', requiredKeys='username,password'):
        super().__init__(file=file, table=table, requiredKeys=requiredKeys)

    def makeUser(self, username: str, password: str) -> int:
        """ creates a user """

        db = self.createObj()
        if db.tbl.contains(Query().username == username):
            db.close()
            raise UsernameExists(f'the username {username} already exists')
        db.close()

        pw = mkpassword(password, urandom(32))

        return self.create({
            'username': username,
            'password': pw
        })

    def testUser(self, userId: int, password: str) -> bool:
        """ tests the password on user id"""
        user = self.readById(userId)
        if user is None:
            return False

        salt = user['password'][:64]
        salt = bytes.fromhex(salt)

        if mkpassword(password, salt) == user['password']:
            return True
        return False

    def authUser(self, username: str, password: str) -> bool:
        """ authenticates a users based on the username and password """
        tdb = self.createObj()
        row = tdb.tbl.get(Query()['username'] == username)
        tdb.close()

        if row is None:
            return False

        return self.testUser(row.doc_id, password)
