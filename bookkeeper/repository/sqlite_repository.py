import sqlite3

from typing import TypeVar, Type
from bookkeeper.repository.abstract_repository import AbstractRepository, T
T = TypeVar('T')
#
# class SQLiteRepository(AbstractRepository[T]):
#     def __init__(self, db_file: str, cls: Type[T]):
#         self.db_file = db_file
#         self.table_name = cls.__name__.lower()
#         self.fields = [f for f in cls.__dict__.keys() if not f.startswith('__')]
#
#         # Подключение к базе данных и создание таблицу, если она не существует.
#         self.conn = sqlite3.connect(self.db_file)
#         self.cursor = self.conn.cursor()
#         self.cursor.execute(f"CREATE TABLE IF NOT EXISTS {self.table_name} ({' '.join([f'{field} TEXT' for field in self.fields])}, pk INTEGER PRIMARY KEY)")
#         self.conn.commit()
#
#     def add(self, obj: T) -> T:
#         # добавление объекта в таблицу
#         fields_str = ', '.join(self.fields)
#         placeholders_str = ', '.join(['?' for _ in self.fields])
#         self.cursor.execute(f"INSERT INTO {self.table_name} ({fields_str}, pk) VALUES ({placeholders_str}, ?)", [getattr(obj, f) for f in self.fields] + [None])
#         pk = self.cursor.lastrowid
#         setattr(obj, 'pk', pk)
#         self.conn.commit()
#         return obj
#
#     def get(self, pk: int) -> T:
#         # Получение объекта с заданным первичным ключом
#         self.cursor.execute(f"SELECT {', '.join(self.fields)} FROM {self.table_name} WHERE pk = ?", (pk,))
#         row = self.cursor.fetchone()
#         if row is None:
#             return None
#         obj = object.__new__(self.cls)
#         for i, field in enumerate(self.fields):
#             setattr(obj, field, row[i])
#         setattr(obj, 'pk', pk)
#         return obj
#
#     def update(self, obj: T) -> T:
#         # Обновление объектов в таблице
#         fields_str = ', '.join([f"{field}=?" for field in self.fields])
#         self.cursor.execute(f"UPDATE {self.table_name} SET {fields_str} WHERE pk=?", [getattr(obj, f) for f in self.fields] + [getattr(obj, 'pk')])
#         self.conn.commit()
#         return obj
#
#     def delete(self, pk: int) -> None:
#         # Удаление объекта с заданным первичным ключом
#         self.cursor.execute(f"DELETE FROM {self.table_name} WHERE pk=?", (pk,))
#         self.conn.commit()

class SQLiteRepository(AbstractRepository[T]):
    def __init__(self, db_file: str, cls: Type[T]):
        self.db_file = db_file
        self.table_name = cls.__name__.lower()
        self.fields = [f for f in cls.__dict__.keys() if not f.startswith('__')]

        # Подключение к базе данных и создание таблицу, если она не существует.
        self.conn = sqlite3.connect(self.db_file)
        self.cursor = self.conn.cursor()
        self.cursor.execute(f"CREATE TABLE IF NOT EXISTS {self.table_name} ({' '.join([f'{field} TEXT' for field in self.fields])}, pk INTEGER PRIMARY KEY)")
        self.conn.commit()

    def add(self, obj: T) -> T:
        # добавление объекта в таблицу
        fields_str = ', '.join(self.fields)
        placeholders_str = ', '.join(['?' for _ in self.fields])
        self.cursor.execute(f"INSERT INTO {self.table_name} ({fields_str}, pk) VALUES ({placeholders_str}, ?)", [getattr(obj, f) for f in self.fields] + [None])
        pk = self.cursor.lastrowid
        setattr(obj, 'pk', pk)
        self.conn.commit()
        return obj

    def get(self, pk: int) -> T:
        # Получение объекта с заданным первичным ключом
        self.cursor.execute(f"SELECT {', '.join(self.fields)} FROM {self.table_name} WHERE pk = ?", (pk,))
        row = self.cursor.fetchone()
        if row is None:
            return None
        obj = object.__new__(self.cls)
        for i, field in enumerate(self.fields):
            setattr(obj, field, row[i])
        setattr(obj, 'pk', pk)
        return obj

    def get_all(self) -> list[T]:
        # Получение списка всех объектов
        self.cursor.execute(f"SELECT pk, {', '.join(self.fields)} FROM {self.table_name}")
        rows = self.cursor.fetchall()
        objs = []
        for row in rows:
            obj = object.__new__(self.cls)
            for i, field in enumerate(self.fields):
                setattr(obj, field, row[i+1])
            setattr(obj, 'pk', row[0])
            objs.append(obj)
        return objs

    def update(self, obj: T) -> T:
        # Обновление объектов в таблице
        fields_str = ', '.join([f"{field}=?" for field in self.fields])
        self.cursor.execute(f"UPDATE {self.table_name} SET {fields_str} WHERE pk=?", [getattr(obj, f) for f in self.fields] + [getattr(obj, 'pk')])
        self.conn.commit()
        return obj

    def delete(self, pk: int) -> None:
        # Удаление объекта с заданным первичным ключом
        self.cursor.execute(f"DELETE FROM {self.table_name} WHERE pk=?", (pk,))
        self.conn.commit()
