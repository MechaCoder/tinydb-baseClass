# file deepcode ignore W0611: <supporting>
from datetime import datetime

from yaml import load, dump

try:
    from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
    from yaml import Loader, Dumper

from tinydb.database import Document
from .exceptions import ExportTypeError


def ymalExport(data: list, exportPath :str):
    """ exports a table into a Ymal file. """
    
    goodrows = []
    for row in data:

        if isinstance(row, Document) is False:
            raise ExportTypeError('the rows list must be popluated with `TinyDB.database.Document`')

        newRow = {'documentId': row.doc_id}
        
        for key in row.keys():
            newRow[key] = row[key]

        goodrows.append(newRow)
    ts = datetime.now()
        
    ymalObj = {
        'export-ts': ts.strftime('%H:%M - %d/%m/%Y'),
        'data': goodrows
    }

    ymalObj = dump(ymalObj)
    with open(exportPath, 'w') as fileObj:
        fileObj.write(ymalObj)
        
    return exportPath