#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Bot for connecting Discord and Alpha-core emulator

Written by Entropy 2021

TODO: Make database independen from Alpha Core
"""

from dotenv import load_dotenv
from mysql.connector import connect, Error # noqa
import os

load_dotenv()


HOST = os.getenv('HOST')
USER = os.getenv('USR')
PASSWORD = os.getenv('PASS')
DATABASE = os.getenv('DB')


class Mysqld:
    def __init__(self, database=DATABASE):
        self.conn = connect(
            host=HOST,
            user=USER,
            password=PASSWORD,
            database=database
        )
        self.cursor = self.conn.cursor(buffered=True)

    def insert(self, SQL, tpl=None, database='Alpha_realm'):
        self.cursor.execute(SQL, tpl)
        id = self.cursor.lastrowid
        self.conn.commit()
        self.conn.close()

        return id

    def delete(self, SQL, tpl=None, database='Alpha_realm'):
        self.cursor.execute(SQL, tpl)
        id = self.cursor.lastrowid
        self.conn.commit()
        self.conn.close()

        return id

    def query(self, SQL, tpl=None):
        result = None

        """if tpl:
            self.cursor.execute(SQL, tpl)
            result = self.cursor.fetchall()
        else:
            self.cursor.execute(SQL)
            result = self.cursor.fetchall()"""

        self.cursor.execute(SQL, tpl)
        result = self.cursor.fetchall()

        self.conn.close()

        return result
