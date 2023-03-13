
import os
import unittest
from bookkeeper.repository.sqlite_repository import SQLiteRepository
import sqlite3
import sqlite3
from bookkeeper.repository.sqlite_repository import SQLiteRepository, TestModel

class TestSQLiteRepository(unittest.TestCase):
    def setUp(self):
        # Создаем временную базу данных для тестов и создаем таблицу в базе данных
        self.db_file = ':memory:'
        conn = sqlite3.connect(self.db_file)
        conn.execute('CREATE TABLE testmodel (id INTEGER PRIMARY KEY, name TEXT, value INTEGER)')
        conn.commit()
        conn.close()
        self.repo = SQLiteRepository(self.db_file, TestModel)

    def tearDown(self):
        # Удаляем временную базу данных
        os.remove(self.db_file)

    def test_add(self):
        # Проверяем добавление объекта в базу данных
        obj = TestModel(name='Test', age=30)
        self.repo.add(obj)
        self.assertIsNotNone(obj.pk)

    def test_get(self):
        # Проверяем получение объекта по первичному ключу
        obj = TestModel(name='Test', age=30)
        self.repo.add(obj)
        result = self.repo.get(obj.pk)
        self.assertEqual(obj.name, result.name)
        self.assertEqual(obj.age, result.age)

    def test_update(self):
        # Проверяем обновление объекта в базе данных
        obj = TestModel(name='Test', age=30)
        self.repo.add(obj)
        obj.name = 'New Name'
        obj.age = 40
        self.repo.update(obj)
        result = self.repo.get(obj.pk)
        self.assertEqual(obj.name, result.name)
        self.assertEqual(obj.age, result.age)

    def test_delete(self):
        # Проверяем удаление объекта из базы данных
        obj = TestModel(name='Test', age=30)
        self.repo.add(obj)
        self.repo.delete(obj.pk)
        result = self.repo.get(obj.pk)
        self.assertIsNone(result)


class TestModel:
    def __init__(self, name: str = None, age: int = None):
        self.pk = None
        self.name = name
        self.age = age


if __name__ == '__main__':
    unittest.main()
