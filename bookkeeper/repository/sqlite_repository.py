import sqlite3
from typing import TypeVar, Type

T = TypeVar('T')

class SQLiteRepository:
    def __init__(self, db_file: str, cls: Type[T]):
        self.db_file = db_file
        self.table_name = cls.__name__.lower()
        self.fields = [f for f in cls.__dict__.keys() if not f.startswith('__')]

        # Connect to the database and create the table if it doesn't exist
        self.conn = sqlite3.connect(self.db_file)
        self.cursor = self.conn.cursor()
        self.cursor.execute(f"CREATE TABLE IF NOT EXISTS {self.table_name} ({' '.join([f'{field} TEXT' for field in self.fields])}, pk INTEGER PRIMARY KEY)")
        self.conn.commit()

    def add(self, obj: T) -> T:
        # Insert the object into the table
        fields_str = ', '.join(self.fields)
        placeholders_str = ', '.join(['?' for _ in self.fields])
        self.cursor.execute(f"INSERT INTO {self.table_name} ({fields_str}, pk) VALUES ({placeholders_str}, ?)", [getattr(obj, f) for f in self.fields] + [None])
        pk = self.cursor.lastrowid
        setattr(obj, 'pk', pk)
        self.conn.commit()
        return obj

    def get(self, pk: int) -> T:
        # Retrieve the object with the given primary key
        self.cursor.execute(f"SELECT {', '.join(self.fields)} FROM {self.table_name} WHERE pk = ?", (pk,))
        row = self.cursor.fetchone()
        if row is None:
            return None
        obj = object.__new__(self.cls)
        for i, field in enumerate(self.fields):
            setattr(obj, field, row[i])
        setattr(obj, 'pk', pk)
        return obj

    def update(self, obj: T) -> T:
        # Update the object in the table
        fields_str = ', '.join([f"{field}=?" for field in self.fields])
        self.cursor.execute(f"UPDATE {self.table_name} SET {fields_str} WHERE pk=?", [getattr(obj, f) for f in self.fields] + [getattr(obj, 'pk')])
        self.conn.commit()
        return obj

    def delete(self, pk: int) -> None:
        # Delete the object with the given primary key
        self.cursor.execute(f"DELETE FROM {self.table_name} WHERE pk=?", (pk,))
        self.conn.commit()
