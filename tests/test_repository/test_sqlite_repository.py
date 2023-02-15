import os
import unittest
from typing import List
from bookkeeper.repository.sqlite_repository import SQLiteRepository

class Person:
    def __init__(self, name: str, age: int):
        self.name = name
        self.age = age
        self.pk = None

class SQLiteRepositoryTests(unittest.TestCase):
    def setUp(self) -> None:
        self.db_file = 'test.db'
        self.repo = SQLiteRepository(self.db_file, Person)

    def tearDown(self) -> None:
        os.remove(self.db_file)

    def test_add(self):
        person = Person('Alice', 30)
        person_added = self.repo.add(person)

        self.assertEqual(person_added.name, 'Alice')
        self.assertEqual(person_added.age, 30)
        self.assertIsNotNone(person_added.pk)

    def test_get(self):
        person1 = Person('Alice', 30)
        person2 = Person('Bob', 25)
        person1_added = self.repo.add(person1)
        person2_added = self.repo.add(person2)

        person1_retrieved = self.repo.get(person1_added.pk)
        person2_retrieved = self.repo.get(person2_added.pk)

        self.assertEqual(person1_retrieved.name, 'Alice')
        self.assertEqual(person1_retrieved.age, 30)
        self.assertEqual(person2_retrieved.name, 'Bob')
        self.assertEqual(person2_retrieved.age, 25)

    def test_update(self):
        person = Person('Alice', 30)
        person_added = self.repo.add(person)

        person_added.name = 'Alice Smith'
        person_updated = self.repo.update(person_added)

        self.assertEqual(person_updated.name, 'Alice Smith')

    def test_delete(self):
        person1 = Person('Alice', 30)
        person2 = Person('Bob', 25)
        person1_added = self.repo.add(person1)
        person2_added = self.repo.add(person2)

        self.repo.delete(person1_added.pk)

        people = self.repo.get_all()
        self.assertEqual(len(people), 1)
        self.assertEqual(people[0].name, 'Bob')

    def test_get_all(self):
        person1 = Person('Alice', 30)
        person2 = Person('Bob', 25)
        person1_added = self.repo.add(person1)
        person2_added = self.repo.add(person2)

        people = self.repo.get_all()

        self.assertEqual(len(people), 2)
        self.assertEqual(people[0].name, 'Alice')
        self.assertEqual(people[0].age, 30)
        self.assertEqual(people[1].name, 'Bob')
        self.assertEqual(people[1].age, 25)

if __name__ == '__main__':
    unittest.main()
