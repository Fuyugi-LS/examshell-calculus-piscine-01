# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
#                                  (      o  )                                #
#                                   \  ‾‾‾  /                                 #
#                                    \_____/                                  #
#                                ─── SciShell ───                             #
#                                                                             #
#    stddb.py                                                                 #
#                                                                             #
#    By: Fuyugi <github.com/Fuyugi-LS>                                        #
#                                                                             #
#    Created: 2025/06/29 09:30:00 by Fuyugi                                   #
#    Updated: 2025/07/06 23:00:00 by Fuyugi                                   #
#                                                                             #
#    © CC0 2025                                                               #
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

from datashell.dirdb import data as _data
import datashell.database as database


class Wrapper:
    introduction = None
    exit = None
    datashell = None
    examshell = None

    @classmethod
    def _set_value(cls):
        __stddict = _data.wrapper
        cls.introduction = __stddict["introduction"]
        cls.exit = __stddict["exit"]
        cls.datashell = __stddict["datashell"]
        cls.examshell = __stddict["examshell"]

    def __init__(self):
        if Wrapper.introduction is None:
            Wrapper._set_value()


class DataShell:
    introduction = None
    exit = None
    schema = None
    sqlcmd = None
    alias = None
    unalias = None

    @classmethod
    def _set_value(cls):
        __stddict = _data.datashell
        cls.introduction = __stddict["introduction"]
        cls.exit = __stddict["exit"]
        cls.schema = __stddict["schema"]
        cls.sqlcmd = __stddict["sqlcmd"]
        cls.alias = __stddict["alias"]
        cls.unalias = __stddict["unalias"]

    def __init__(self):
        if DataShell.introduction is None:
            DataShell._set_value()


class alias(database.Alias):
    pass


def init_database() -> None:
    _data.init_data()
    alias()


__all__ = (init_database, Wrapper, DataShell)
