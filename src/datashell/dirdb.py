# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
#                                  (      o  )                                #
#                                   \  ‾‾‾  /                                 #
#                                    \_____/                                  #
#                                ─── SciShell ───                             #
#                                                                             #
#    dirdb.py                                                                 #
#                                                                             #
#    By: Fuyugi <github.com/Fuyugi-LS>                                        #
#                                                                             #
#    Created: 2025/06/29 09:30:00 by Fuyugi                                   #
#    Updated: 2025/07/06 23:00:00 by Fuyugi                                   #
#                                                                             #
#    © CC0 2025                                                               #
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

import json
import csv
import sqlite3


class _stdpath:
    __data = "../data/"
    wrapper = "{}wrapper.json".format(__data)
    datashell = "{}datashell.json".format(__data)
    database = "{}database.db".format(__data)


class data:
    wrapper = None
    datashell = None

    @staticmethod
    def __json_dictfinder(path: str):
        r: dict
        with open(path, 'r', encoding='utf-8') as f:
            r = json.load(f)
        return r

    @staticmethod
    def __sqlite3_init():
        dbsql = sqlite3.connect(_stdpath.database)
        db = sqlite3.Cursor(dbsql)
        for f in data.datashell["schema"]:
            db.execute(data.datashell["schema"][f])
        dbsql.commit()
        dbsql.close()

    @classmethod
    def init_data(cls):
        cls.wrapper = cls.__json_dictfinder(_stdpath.wrapper)
        cls.datashell = cls.__json_dictfinder(_stdpath.datashell)
        cls.db = cls.__sqlite3_init()
