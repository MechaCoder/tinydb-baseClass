# TinyDB base

I use TinyDB ... a lot and very often and i seem to be writing the same functions over and over. The idea behind the small project to provide a way for devs to easily create a data modal around tinydb without the need to build a base class.

## Important

+ BREAKING CHANGE; there is a breaking in `tinydb_base.bata.DatabaseBase`, i have changed that way you define column heads in tables they are now a csl (comma separated list)

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

        def __init__(self, file='ds.json', table=__name__, requiredKeys='title,myContent'):
            super().__init__(file=file, table=table, requiredKeys=requiredKeys)


    MyTable().create({'title': 'foobar', 'myContent': 'this is a string'})

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
|clear||this removes all data from the table|

### DatabaseBaseSercure

this works exactly the same way as `DatabaseBase` but by providing a salt you can encrypt using Fernet, it is suggested that you define your own salt

``` python 3

from tinydb_base.cryptography import DatabaseBaseSercure


class Diary(DatabaseBaseSercure):

    def __init__(self, file='ds.json', table=__name__, requiredKeys='title,content', salt='salt'):
        super().__init__(file=file, table=table, requiredKeys=requiredKeys, salt=salt)


obj = Diary(salt='thisisasalt')
```

|Method Name| attr | Description |
|---|---|---|
|create| dict | this adds a new row to the database.
|createMultiple| list of dicts | this added multiple rows|
|readAll|| returns a list obj|
|readById|id| this gets a row by the id |
|removeById|id|this removes a row by id |
|clear||this removes all data from the table|

### User
Something that alot of systems need to is work with user componants, this is a
simple class that enables Users to be created, it is a class that is inherted
from `DatabaseBase`, but has speail methods that pertain to Users

``` Python 3

from tinydb_base import User
usrTable = User() # will work with a user as a table,
>>> usrTable.makeUser('me', 'mypassword')
1
>>> usrTable.authUser('me', '!mypassword')
False
>>> usrTable.authUser('me', 'mypassword')
True

```

|Method Name| attr | Description |
|---|---|---|
|makeUser| username, password | creates a user in the system|
|testUser| userId, password | tests a password angest a user id|
|authUser| username, password| test a username and password|


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

#### defualting keys

if you need to have keys in your data file, you can make sure that they exist.

``` python 3

from tinydb_base.getSet import GetSet

class Settings(GetSet):

    def __init__(self, salt, pw, file='ds.json', table=__name__):
        super().__init__(salt, pw, file=file, table=table)
        self.defaultRows({
            'foo': 'bar'
        })

```

### GetSetSercure

Works the same as `GetSet` but both the tags and the values encrypted.

```python 3

from tinydb_base.getSetSercure import GetSetSercure

class PasswordCode(GetSetSercure):

    def __init__(self, salt, pw, file='ds.json', table=__name__):
        super().__init__(salt, pw, file=file, table=table)

obj = PasswordCode('salty', 'notasercurepassword').set('foo', 'bar')

```

### exporting table to File

these functions export a list of documents into JSON or Ymal, the functions take a list of `documents` and the export path. this will create a file that has all the data and a human-readable time date stamp.

``` python 3

from tinydb_base.exporter import jsonExport
from tinydb_base.exporter import ymalExport
from tinydb_base import DatabaseBase

a = DatabaseBase()

for index in range(0, 10):
    a.create({'title': index})

b = jsonExport(a.readAll(), 'jsonData.json')
b = ymalExport(a.readAll(), 'ymalData.ymal')


```
