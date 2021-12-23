from datetime import datetime

from tinydb import Query

from .factory import Factory
from .exceptions import RowNotFound_Exception
from .data import mkPath


def futureTimeStamp(
    day: int = 0,
    month: int = 0,
    year: int = 0,
    hour: int = 0,
    minute: int = 0,
    second: int = 0
):
    nowTs = datetime.now()
    return datetime(
        day=nowTs.day + day,
        month=nowTs.month + month,
        year=nowTs.year + year,
        hour=nowTs.hour + hour,
        minute=nowTs.minute + minute,
        second=nowTs.second + second,
        microsecond=nowTs.microsecond
    )


class GetSet:

    def __init__(self, file: str = 'ds.json', table: str = __name__):
        super().__init__()

        self.fileName = mkPath(file)
        self.tableName = table
        self.defaultRows({})

    def _checkTimeout(self):
        factory = Factory(self.fileName, self.tableName)
        timeStamp = datetime.now().timestamp()

        for row in factory.tbl.all():

            if isinstance(row['timeout'], float):

                if row['timeout'] <= timeStamp:
                    factory.tbl.remove(doc_ids=[row.doc_id])

        factory.close()
        return True

    def defaultRows(self, dRows: dict) -> None:
        """ runs on instance - adds any rows only if the tag dose not exist, takes a dict"""
        factory = Factory(self.fileName, self.tableName)
        for tag in dRows.keys():
            if factory.tbl.contains(Query().tag == tag) is False:
                self.set(tag, dRows[tag])
        factory.close()

    def set(self, tag: str, value: str, timeout: datetime = None) -> int:
        """ sets data by tag"""

        newRow = {
            'tag': tag,
            'val': value,
            'timeout': None
        }

        if isinstance(timeout, datetime):
            newRow['timeout'] = timeout.timestamp()

        obj = Factory(self.fileName, self.tableName)
        rowId = obj.tbl.upsert(newRow, Query().tag == tag)
        obj.close()
        self._checkTimeout()
        return rowId[0]

    def get(self, tag: str) -> str:
        """ get the row by Tag """

        obj = Factory(self.fileName, self.tableName)
        self._checkTimeout()
        if obj.tbl.contains(Query().tag == tag) is False:
            obj.close()
            raise RowNotFound_Exception('row has not been found.')

        row = obj.tbl.get(Query().tag == tag)
        obj.close()
        return row['val']
