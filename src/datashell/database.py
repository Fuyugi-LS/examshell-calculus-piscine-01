# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
#                                  (      o  )                                #
#                                   \  ‾‾‾  /                                 #
#                                    \_____/                                  #
#                                ─── SciShell ───                             #
#                                                                             #
#    database.py                                                              #
#                                                                             #
#    By: Fuyugi <github.com/Fuyugi-LS>                                        #
#                                                                             #
#    Created: 2025/06/29 09:30:00 by Fuyugi                                   #
#    Updated: 2025/07/06 23:00:00 by Fuyugi                                   #
#                                                                             #
#    © CC0 2025                                                               #
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

import sqlite3
import datashell.dirdb as dirdb


class Alias:
    _cmd = None
    _select = None
    _insert = None
    _delete = None

    def __init__(self):
        if Alias._cmd is None:
            Alias._cmd = dirdb.data.datashell["sqlcmd"]["alias"]
            Alias._select = Alias._cmd["select"]
            Alias._insert = Alias._cmd["insert"]
            Alias._delete = Alias._cmd["delete"]

    @staticmethod
    def select(name: str) -> tuple:
        cmd: str
        dbsql = sqlite3.connect(dirdb._stdpath.database)
        db = sqlite3.Cursor(dbsql)
        db.execute(Alias._select, (name,))
        cmd = db.fetchone()
        dbsql.close()
        return cmd

    @staticmethod
    def insert(alias_input: dict) -> None:
        dbsql = sqlite3.connect(dirdb._stdpath.database)
        db = sqlite3.Cursor(dbsql)
        db.execute(Alias._insert,
                   (alias_input["name"].strip(), alias_input["cmd"].strip()))
        dbsql.commit()
        dbsql.close()

    @staticmethod
    def delete(name: str) -> None:
        dbsql = sqlite3.connect(dirdb._stdpath.database)
        db = sqlite3.Cursor(dbsql)
        db.execute(Alias._delete, (name,))
        dbsql.commit()
        dbsql.close()
