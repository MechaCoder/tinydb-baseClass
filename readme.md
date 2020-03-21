# TinyDB base

I use TinyDB ... a lot and very often and i seem to be writing the same functions over and over. The idea behind the small project to provide a way for devs to easily create a data modal around tinydb without the need to build a base class.

## How to install

the easiest way is to install through your dependency manager `pip install tinyDbBase` or if using `pipenv install tinyDbBase`.

## How do i use this thing

### Factory

This allows you to interact with Tinydb and both the root object and a table in the same object.

```python 3

    from tinydb_base import Factory

    db = Factory('myData.json', 'myTable')
    db.db # equliervent to `TinyDB`.
    db.tbl # equliervent to `TinyDB.Table`.

    db.close() # closes the database file.

 ```

### DatabaseBase

the idea is to import the base class and then derives into your own class. the idea is that you can simply create your data layer by creating a class that will work out what needs and just work.

``` python 3

    from tinydb_base import DatabaseBase

    class MyTable(DatabaseBase):

        def __init__(self, file='ds.json', table=__name__, requiredKeys=['title']):
            super().__init__(file=file, table=table, requiredKeys=requiredKeys)


    MyTable().create({'title': 'foobar'})

```

This will enable to accesses the base class, you can add your own custom functions. the will use the namespaces of the file within the project, but you can override this easily at an instance. another cool feature is that required keys this is key that must be present in every row which can also be changed.

#### methods

|Method Name| attr | Description |
|---|---|---|
|create| dict | this adds a new row to the database.
|createMultiple| list of dicts | this added multiple rows|
|readAll|| returns a list obj|
|readById|id| this gets a row by the id |
|removeById|id|this removes a row by id |

### DatabaseBaseSercure

this works exactly the same way as `DatabaseBase` but by providing a salt you can encrypt using Fernet, it is suggested that you define your own salt

``` python 3

from tinydb_base.cryptography import DatabaseBaseSercure


class Diary(DatabaseBaseSercure):

    def __init__(self, file='ds.json', table=__name__, requiredKeys=['title'], salt='salt'):
        super().__init__(file=file, table=table, requiredKeys=requiredKeys, salt=salt)


obj = Diary(salt='thisisasalt')
```

### GetSet

this is a very simple interface that sets and gets values based on a tag. this can be used for things like settings. if the tag dose did not exist the class will raise `tinydb_base.exceptions.RowNotFound_Exception`

```python 3
from tinydb_base.getSet import GetSet

class Settings(GetSet):

    def __init__(self, file: str = 'ds.json', table: str = __name__):
        super().__init__()

Settings().set('foo', 'bar')
Settings().get('foo')
```
