from tinydb.database import Document


def exportToDict(row: Document) -> dict:
    """ export passed document to a dict """

    if isinstance(row, Document) is False:
        raise TypeError('the row must be dict')

    newRow = {}
    newRow['doc_id'] = row.doc_id

    for key in row.keys():
        newRow[key] = row[key]

    return newRow


def exportToListOfDicts(lis: list) -> list:
    """ exports a list of documents to a list of dicts """

    if isinstance(lis, list) is False:
        raise TypeError('the lis need to be a list')

    newRows = []
    for row in lis:

        tempRow = exportToDict(row)
        newRows.append(tempRow)

    return newRows
