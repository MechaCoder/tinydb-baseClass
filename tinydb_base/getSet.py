from tinydb import Query

from .factory import Factory
from .exceptions import RowNotFound_Exception


class GetSet:

    def __init__(self, file: str = 'ds.json', table: str = __name__):
        super().__init__()

        self.fileName = file
        self.tableName = table

    def set(self, tag: str, value: str):
        """ sets data by tag"""

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

        if obj.tbl.contains(Query().tag == tag) is False:
            obj.close()
            raise RowNotFound_Exception('row has not been found.')

        row = obj.tbl.get(Query().tag == tag)
        obj.close()
        return row['val']
