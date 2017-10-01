import sqlite3

from time import time


class AnalyticsDB:
    def __init__(self):
        self.db = sqlite3.connect("analytics.db")
        self.c = self.db.cursor()
        self.create_tables()

    def create_tables(self):
        self.c.execute("""
            CREATE TABLE IF NOT EXISTS installed
                (id INTEGER PRIMARY KEY AUTOINCREMENT, date INTEGER, version TEXT, country TEXT,
                ip INTEGER, uuid TEXT, mmcdir TEXT, installdir TEXT, system TEXT)
        """)

        self.c.execute("""
            CREATE TABLE IF NOT EXISTS crashes
                (id INTEGER PRIMARY KEY AUTOINCREMENT, date INTEGER, exception TEXT, email TEXT, notes TEXT,
                uuid TEXT, version TEXT)
        """)

        self.db.commit()

    def insert_anal(self, ver: str, country: str, ip: int, uuid: str, mmc: str, install: str, sys: str):
        self.c.execute("""
            INSERT INTO installed(date,version,country,ip,uuid,mmcdir,installdir,system) VALUES (?,?,?,?,?,?,?,?)
        """, (int(time()*1000), ver, country, ip, uuid, mmc, install, sys))

        self.db.commit()

    def insert_crash(self, ver: str, exc: str, email: str, notes: str, uuid: str):
        self.c.execute("""
            INSERT INTO installed(date,exception,email,notes,uuid,version) VALUES (?,?,?,?,?,?)
        """, (int(time()*1000), exc, email, notes, uuid, ver))

        self.db.commit()

    def select(self, statement):
        self.c.execute(statement)
        return self.c.fetchall()
