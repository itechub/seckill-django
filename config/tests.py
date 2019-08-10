#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2019 root <root@MrRobot.local>
#

"""
Test Basic Project Setup
"""

from django.db import connections
from django.db.utils import OperationalError
from django.test import TestCase


class DBConnectionTest(TestCase):
    db_conn = connections["default"]

    def test_db_connectivity(self):
        try:
            DBConnectionTest.db_conn.cursor()
        except OperationalError:
            connected = False
        else:
            connected = True
        self.assertTrue(connected)

    def test_db_char_encoding(self):
        with DBConnectionTest.db_conn.cursor() as cursor:
            cursor.execute("show create database seckill;")
            row = cursor.fetchone()
        self.assertIn("utf8mb4", str(row))
