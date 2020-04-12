from datetime import datetime
from json import dumps

from tinydb.database import Document

from .exceptions import ExportTypeError

def jsonExport(rows: list, exportPath: str):
    """ Exports a table list data to a json file. """

    if isinstance(rows, list) is False:
        raise ExportTypeError('the rows must be a list')

    if isinstance(exportPath, str) is False:
        raise ExportTypeError('the export path must be a string')

    rowsExport = []
    for row in rows:

        if isinstance(row, Document) is False:
            raise ExportTypeError('the rows list must be popluated with `TinyDB.database.Document`')

        newRow = {'documentId': row.doc_id}
        for key in row.keys():
            newRow[key] = row[key]

        rowsExport.append(newRow)
    ts = datetime.now()

    jsonObj = {
        'export-ts': ts.strftime('%H:%M - %d/%m/%Y'),
        'data': rowsExport
    }
    jsonObj = dumps(jsonObj, sort_keys=True, indent=4, separators=(',', ': '))
    with open(exportPath, 'w') as fileObj:
        fileObj.write(jsonObj)

    return exportPath

