# file deepcode ignore W0611: this is a test running file and connects a runtime to all testing in the project

from unittest import main
from tests.testFactory import TestFactory
from tests.testData import TestData
from tests.testOutput import TestExport
from tests.testCryptography import TestFernetFactory, TestDatabaseBaseSercure
from tests.testGetSet import TestGetSet
from tests.testGetSetSercure import TestGetSetSercure
from tests.testExporter import TestExporter
from tests.testUser import TestUser

if __name__ == '__main__':
    main()
