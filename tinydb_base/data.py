from datetime import datetime
from .factory import Factory
from tinydb.database import Document
from tinydb import Query

from os.path import join, abspath, dirname

def mkPath(file:str = 'Pipfile'):
    return join(abspath(dirname('.')), file)

class DatabaseBase:

    def __init__(self, file: str = 'ds.json', table: str = __name__, requiredKeys='title:str'):
        super().__init__()

        self.fileName = mkPath(file=file)
        self.table = table

        columnTypes = {}
        for column in requiredKeys.split(','):
            col = column.split(':')
            if len(col) == 1:
                col.append('str')
            columnTypes[col[0]] = col[1]

        self.requiredKeys = columnTypes

        self.createObj = lambda: Factory(self.fileName, self.table)
        self.now_ts = lambda: datetime.now().timestamp()

    def _typeCheck(self, header:str, value:any) -> bool:
        
        if header not in self.requiredKeys.keys():
            return False

        testVal = None
        if self.requiredKeys[header] == 'str':
            testVal = str
        elif self.requiredKeys[header] == 'int':
            testVal = int
        elif self.requiredKeys[header] == 'bool':
            testVal = bool
        elif self.requiredKeys[header] == 'float':
            testVal = float
        else:
            raise TypeError('the excepted types are string, intger, float or boolen, ')

        if isinstance(value, testVal):
            return True
        return False



    def create(self, row: dict) -> int:
        """ inserts a single row into the database """

        if isinstance(row, dict) is False:
            raise TypeError('the row must be a dict')

        if row == {}:
            raise TypeError('the row must have key value pair.')

        for e in row.keys():
            if e not in self.requiredKeys.keys():
                raise KeyError(
                    'a required key ({}) has not been found in the row'.format(e)
                )
            
            if self._typeCheck(e, row[e]) == False:
                raise TypeError('the header is not the correct type.')


        db = self.createObj()
        rid = db.tbl.insert(row)
        db.close()

        return rid

    def createMultiple(self, rows: list) -> list:
        """ adds multipe rows to the database in one go """

        if isinstance(rows, list) is False:
            raise TypeError('the rows to be added must be in a list')

        goodrows = []
        for row in rows:

            if isinstance(row, dict) is False:
                raise Warning('all rows must be a dict SKIPING')

            for key in row.keys():  # checking the required keys are present.
                if key not in self.requiredKeys.keys():
                    raise Warning(
                        'all rows must be have all required keys ({}) SKIPING'.format(key))

                if self._typeCheck(key, row[key]) == False:
                    raise TypeError('the header is not the correct type.')

            
            goodrows.append(row)

        db = self.createObj()
        newIds = db.tbl.insert_multiple(goodrows)
        db.close()
        return newIds

    def readAll(self) -> list:
        """ returns all rows as tinydb.document"""
        db = self.createObj()
        rows = db.tbl.all()
        db.close()
        return rows

    def readById(self, doc_id: int) -> Document:
        """ reads a row by the document_id """

        if isinstance(doc_id, int) is False:
            raise TypeError('the doc_id must be a int')
        db = self.createObj()
        row = db.tbl.get(doc_id=doc_id)
        db.close()
        return row

    def updateById(self, doc_id: int, tag: str, value: any) -> int:
        db = self.createObj()
        updatedIds = db.tbl.update({tag: value}, doc_ids=[doc_id])
        db.close()
        return updatedIds[0]

    def removeById(self, doc_id: int) -> bool:
        """ removes the row by the document_id """

        if isinstance(doc_id, int) is False:
            raise TypeError('the doc_id must be a int')
        db = self.createObj()
        db.tbl.remove(doc_ids=[doc_id])
        db.close()
        return True

    def clear(self) -> bool:
        """ clears all data in tables from db file. """
        tdb = self.createObj()
        try:
            tdb.db.drop_table(self.table)  # python36
        except AttributeError:
            tdb.db.purge_table(self.table)  # python37, python38
        tdb.close()
        return True

    def exists(self, tag: str, value: any) -> bool:
        """ 
        checks of a row exists by querying a tag by a value
        """

        if tag not in self.requiredKeys:
            raise TypeError('tag is not in required keys')

        db = self.createObj()
        result = db.tbl.contains(Query()[tag] == value)
        db.close()

        return result
