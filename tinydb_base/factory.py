from tinydb import TinyDB


class Factory:

    def __init__(self, file: str, table: str = '_default'):
        """
            this a Object factory this allows a user to access the TinyDB object, and TinyDB.table
            useing a simple api
        """
        super().__init__()

        if isinstance(file, str) is False:
            raise TypeError('The file path must be a string')

        if isinstance(table, str) is False:
            raise TypeError('the table must be a string')

        self.db = TinyDB(file)
        self.tbl = self.db.table(table)

    def close(self) -> bool:
        """ this closes this a files """
        self.db.close()
        return True
