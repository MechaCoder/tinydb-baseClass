from tinydb import Query

from .factory import Factory


class DatabaseBase:

    def __init__(self, file: str = 'ds.json', table: str = __name__, requiredKeys=['title']):
        super().__init__()

        self.fileName = file
        self.table = table
        self.requiredKeys = requiredKeys

        self.createObj = lambda: Factory(self.fileName, self.table)

    def create(self, row: dict):
        """ inserts a single row into the database """

        if isinstance(row, dict) is False:
            raise TypeError('the row must be a dict')

        for e in row.keys():
            if e not in self.requiredKeys:
                raise KeyError('a required key has not been found in the row')

        db = self.createObj()
        rid = db.tbl.insert(row)
        db.close()

        return rid

    def createMultiple(self, rows: list):
        """ adds multipe rows to the database in one go """

        if isinstance(rows, list) is False:
            raise TypeError('the rows to be added must be in a list')

        goodrows = []
        for row in rows:

            if isinstance(row, dict) is False:
                raise Warning('all rows must be a dict SKIPING')
                continue

            for key in row.keys():  # checking the required keys are present.
                if key not in self.requiredKeys:
                    raise Warning(
                        'all rows must be have all required keys SKIPING')
                    continue
            goodrows.append(row)

        db = self.createObj()
        newIds = db.tbl.insert_multiple(goodrows)
        db.close()
        return newIds

    def readAll(self):
        """ returns all rows as tinydb.document"""
        db = self.createObj()
        rows = db.tbl.all()
        db.close()
        return rows

    def readById(self, doc_id: int):
        """ reads a row by the document_id """

        if isinstance(doc_id, int) is False:
            raise TypeError('the doc_id must be a int')
        db = self.createObj()
        row = db.tbl.get(doc_id=doc_id)
        db.close()
        return row

    def removeById(self, doc_id: int):
        """ removes the row by the document_id """

        if isinstance(doc_id, int) is False:
            raise TypeError('the doc_id must be a int')
        db = self.createObj()
        db.tbl.remove(doc_ids=[doc_id])
        db.close()
        return True
