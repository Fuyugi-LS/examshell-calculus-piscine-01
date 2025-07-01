# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
#                                  (      o  )                                #
#                                   \  ‾‾‾  /                                 #
#                                    \_____/                                  #
#                                ─── SciShell ───                             #
#                                                                             #
#    path.py                                                                  #
#                                                                             #
#    By: Fuyugi <github.com/Fuyugi-LS>                                        #
#                                                                             #
#    Created: 2025/06/29 09:30:00 by Fuyugi                                   #
#    Updated: 2025/07/06 23:00:00 by Fuyugi                                   #
#                                                                             #
#    © CC0 2025                                                               #
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

from utils.globals import *


class __SERVICE__:
    @staticmethod
    def create_global_path(name: str) -> str:
        out = _L_PROGRAM_FILE_ + name + '/'
        return out

    @staticmethod
    def create_local_path(name: str) -> str:
        out = _G_PROGRAM_FILE_ + name + '/'
        return out

    @staticmethod
    def getpath(isglobal: bool, name: str) -> str:
        out = None
        match isglobal:
            case True:
                out = __SERVICE__.create_global_path
            case False:
                out = __SERVICE__.create_local_path
            case _:
                raise SystemError("Invalid isglobal value")
        return out(name)


def scishell(isglobal: bool) -> str:
    out = __SERVICE__.getpath
    return out(isglobal, 'scishell')


def datashell(isglobal: bool):
    out = __SERVICE__.getpath
    return out(isglobal, 'datashell')


def examshell(isglobal: bool):
    out = __SERVICE__.getpath
    return out(isglobal, 'examshell')


def program_file(isglobal: bool):
    out = __SERVICE__.getpath
    return out(isglobal, 'program_file')
