# TinyDB base

I use TinyDB ... a lot and very offen and i seam to be writeing the same functions over and over. The idea behind the small project to provide a way for devs to easly create a data modal around tinydb without the need to build a base class.

## How to install

the easyest way is to install though your dependicy maniger `pip install tinyDbBase` or if useing `pipenv install tinyDbBase`.

## How do i use this thing

### DatabaseBase

the idea is import the baseclass and then inherits into your own class. the idea is that you can simply create your data layer by creating class that will work out what needs and just work.

``` python 3

    class MyTable(DatabaseBase):

        def __init__(self, file='ds.json', table=__name__, requiredKeys=['title']):
            super().__init__(file=file, table=table, requiredKeys=requiredKeys)


    MyTable().create({'title': 'foobar'})

```

This will enable to acesses the base class, you can add your own custom fuctions. the will use the name spaces of file with in the project, but you can override this easly at instance. anouther cool feature is that requiredKeys this is key that must be present in every row which can also be changed.

### DatabaseBaseSercure

this works excatly the same way as `DatabaseBase` but by provideing a salt you can encript useing Fernet, it is suggestioned that you define your own salt

``` python 3

from tinyDbBase.cryptography import DatabaseBaseSercure


class Diary(DatabaseBaseSercure):

    def __init__(self, file='ds.json', table=__name__, requiredKeys=['title'], salt='salt'):
        super().__init__(file=file, table=table, requiredKeys=requiredKeys, salt=salt)


obj = Diary(salt='thisisasalt')

```

## methods

|Method Name| attr | Description |
|---|---|---|
|create| dict | this adds a new row to the database.
|createMultiple| list of dicts | this added multiple rows|
|readAll|| returns a list obj|
|readById|id| this gets a row by the id |
|removeById|id|this removes a row by id |
