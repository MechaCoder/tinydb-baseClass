from .factory import Factory
from .cryptography import FernetFactory
from .exceptions import RowNotFound_Exception


class GetSetSercure:

    def __init__(self, salt: str, pw: str, file: str = 'ds.json', table: str = __name__):
        super().__init__()

        self.fileName = file
        self.tableName = table
        self.salt = salt
        self.pw = pw

    def _tagList(self):
        """ returns a list of the tags """
        fernet = FernetFactory(self.pw, self.salt)
        obj = Factory(self.fileName, self.tableName)

        cleanRows = []
        for row in obj.tbl.all():
            cleanRows.append({
                'ident': row.doc_id,
                'tag': fernet.decrypt(row['tag'])
            })
        obj.close()
        return cleanRows

    def _updateValueById(self, ident: int, tag: str, newValue: str) -> bool:

        obj = Factory(self.fileName, self.tableName)
        fernet = FernetFactory(self.pw, self.salt)
        s_newVal = fernet.encrypt(newValue)
        s_tag = fernet.encrypt(tag)
        obj.tbl.update({'tag': s_tag, 'val': s_newVal}, doc_ids=[ident])
        obj.close()
        return True

    def set(self, tag: str, value: str) -> bool:
        """ sets data by tag"""

        fernet = FernetFactory(self.pw, self.salt)

        tagFound = False
        for row in self._tagList():
            if row['tag'] is tag:
                tagFound = True
                self._updateValueById(row['ident'], tag, value)

        if tagFound:
            return True
        obj = Factory(self.fileName, self.tableName)
        obj.tbl.insert({
            'tag': fernet.encrypt(tag),
            'val': fernet.encrypt(value)
        })
        obj.close()
        return True

    def get(self, tag: str) -> str:
        """ get the row by Tag """

        obj = Factory(self.fileName, self.tableName)
        fernet = FernetFactory(self.pw, self.salt)
        stag = fernet.encrypt(tag)

        returnVal = ''
        for row in obj.tbl.all():
            if fernet.decrypt(row['tag']) == tag:
                returnVal = fernet.decrypt(row['val'])
                break
        if returnVal == '':
            raise RowNotFound_Exception('tag has not been found')
        obj.close()
        return returnVal
