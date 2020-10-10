from base64 import urlsafe_b64encode

from cryptography.fernet import Fernet, InvalidToken
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from tinydb.database import Document

from .data import DatabaseBase
from .factory import Factory


class FernetFactory:

    def __init__(self, password: str, salt: str):
        super().__init__()
        self.key = self._mkKey(password, salt)

    def _mkKey(self, password: str, salt: str) -> str:

        if isinstance(password, str) is False:
            raise TypeError('the password needs to be a string')

        if isinstance(salt, str) is False:
            raise TypeError('the salt must be a string')

        ps = password.encode()
        salt = salt.encode()
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
            backend=default_backend()
        )
        key = urlsafe_b64encode(kdf.derive(ps))

        return key

    def encrypt(self, msg: str) -> str:
        fernet = Fernet(self.key)

        if isinstance(msg, str) is False:
            msg = str(msg)

        msg = msg.encode()
        return fernet.encrypt(msg).decode()

    def decrypt(self, token: str) -> str:
        fernet = Fernet(self.key)
        token = token.encode()
        return fernet.decrypt(token).decode()


class DatabaseBaseSercure(DatabaseBase):

    def __init__(self, file='ds.json', table=__name__, requiredKeys='title', salt='salt'):
        super().__init__(file=file, table=table, requiredKeys=requiredKeys)
        self.salt = salt

    def create(self, row: dict, pw: str) -> int:
        """ creates a row where the keys and values are encripted"""

        if isinstance(pw, str) is False:
            raise TypeError('the password must be a string')

        if isinstance(row, dict) is False:
            raise TypeError('the row must be a dict')

        for key in row.keys():
            if key not in self.requiredKeys:
                raise KeyError(
                    'a required key ({}) has not been found in the row'.format(key))

        newRow = {}
        fernet = FernetFactory(pw, self.salt)

        for key in row.keys():

            value = str(row[key])  # converts every value to a string
            value = fernet.encrypt(value)

            key = str(key)
            key = fernet.encrypt(key)
            newRow[key] = value

        fact = Factory(self.fileName, self.table)
        newId = fact.tbl.insert(newRow)
        fact.close()

        return newId

    def createMultiple(self, rows: list, pw: str) -> list:
        """ adds multiple rows to the database where the keys and value"""

        if isinstance(rows, list) is False:
            raise TypeError('the list of rows need to be a list')

        if isinstance(pw, str) is False:
            raise TypeError('the password needs to be a string')

        fernet = FernetFactory(pw, self.salt)

        newRows = []
        for row in rows:

            newRow = {}
            for key in row.keys():
                if key not in self.requiredKeys:
                    raise Warning(
                        'a required key ({}) has not been found in the row'.format(key))

                newKey = fernet.encrypt(key)
                newVal = fernet.encrypt(row[key])

                newRow[newKey] = newVal

            newRows.append(newRow)
        db = Factory(self.fileName, self.table)
        rowids = db.tbl.insert_multiple(newRows)
        db.close()

        return rowids

    def readAll(self, pw: str) -> list:
        """ returns all rows that are decriptable with the passed password """
        goodRows = []
        fernet = FernetFactory(pw, self.salt)
        for row in super().readAll():
            newrow = {
                'doc_id': row.doc_id
            }

            for key in row.keys():
                try:
                    newkey = fernet.decrypt(key)
                except InvalidToken:
                    continue

                try:
                    newVal = fernet.decrypt(row[key])
                except InvalidToken:
                    continue

                newrow[newkey] = newVal

            if newrow == {}:
                continue
            goodRows.append(newrow)
        return goodRows

    def readById(self, doc_id: int, pw: str) -> Document:
        """ get the row to decript """
        row = super().readById(doc_id)
        if row is None:
            raise TypeError('row not found')

        newRow = {
            'doc_id': row.doc_id
        }
        fernet = FernetFactory(pw, self.salt)
        for key in row.keys():
            newKey = fernet.decrypt(key)
            newValue = fernet.decrypt(row[key])
            newRow[newKey] = newValue

        return newRow
