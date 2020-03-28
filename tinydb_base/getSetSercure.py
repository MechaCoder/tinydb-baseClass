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

    def set(self, tag: str, value: str):
        """ sets data by tag"""

        fernet = FernetFactory(self.pw, self.salt)
        try:
            
            self.get(tag) # if the row dose not exist will raise a RowNotFound_Exception
            rowId = None
            db = Factory(self.fileName, self.tableName)
            for row in obj.tab.all():
                if fernet.decrypt(row['tag']) == tag:
                    rowId = row.doc_id
            
            if rowId is None:
                raise RowNotFound_Exception()
            
            sValue = fernet.encrypt(value)
            db.tbl.update({'val': sValue}, doc_ids=[rowId])
            db.close()
            
        except RowNotFound_Exception:
            db2 = Factory(self.fileName, self.tableName)
            sTag = fernet.encrypt(tag)
            SVal = fernet.encrypt(value)
            db2.tbl.insert({'tag': sTag, 'val': SVal})
            db2.close()
        return True

    def get(self, tag: str):
        """ get the row by Tag """

        obj = Factory(self.fileName, self.tableName)
        fernet = FernetFactory(self.pw, self.salt)
        stag = fernet.encrypt(tag)

        returnVal = ''
        for row in obj.tbl.all():
            if fernet.decrypt(row['tag']) == tag:
                returnVal = fernet.decrypt(row['val'])
                break
        if returnVal is '':
            raise RowNotFound_Exception('tag has not been found')
        obj.close()
        return returnVal
