from tinydb import Query

from .factory import Factory
from .getSet import GetSet
from .cryptography import FernetFactory
from .exceptions import RowNotFound_Exception


class GetSetSercure:

    def __init__(self, salt: str, pw: str, file: str = 'ds.json', table: str = __name__):
        super().__init__()

        self.fileName = file
        self.tableName = table
        self.salt = salt
        self.pw = pw
        self.defaultRows({})

    def defaultRows(self, dRows: dict):
        """ runs on instance - adds any rows only if the tag dose not exist, takes a dict"""
        factory = Factory(self.fileName, self.tableName)
        for tag in dRows.keys():
            if factory.tbl.contains(Query().tag == tag) is False:
                self.set(tag, dRows[tag])
        factory.close()

    def set(self, tag: str, value: str):
        """ sets data by tag"""

        fernet = FernetFactory(self.pw, self.salt)
        tag = fernet.encrypt(tag)
        value = fernet.encrypt(value)

        obj = Factory(self.fileName, self.tableName)
        rowId = obj.tbl.upsert({
            'tag': tag,
            'val': value
        }, Query().tag == tag)
        obj.close()
        return rowId[0]

    def get(self, tag: str):
        """ get the row by Tag """

        obj = Factory(self.fileName, self.tableName)
        fernet = FernetFactory(self.pw, self.salt)
        tag = fernet.encrypt(tag)

        if obj.tbl.contains(Query().tag == tag) is False:
            obj.close()
            raise RowNotFound_Exception('row has not been found.')

        row = obj.tbl.get(Query().tag == tag)
        returnVal = fernet.decrypt(row['val'])
        obj.close()
        return returnVal
