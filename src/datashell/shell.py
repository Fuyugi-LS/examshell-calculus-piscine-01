# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
#                                  (      o  )                                #
#                                   \  ‾‾‾  /                                 #
#                                    \_____/                                  #
#                                ─── SciShell ───                             #
#                                                                             #
#    shell.py                                                                 #
#                                                                             #
#    By: Fuyugi <github.com/Fuyugi-LS>                                        #
#                                                                             #
#    Created: 2025/06/29 09:30:00 by Fuyugi                                   #
#    Updated: 2025/07/06 23:00:00 by Fuyugi                                   #
#                                                                             #
#    © CC0 2025                                                               #
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

import cmd
from datashell import *


class __MAIN__(cmd.Cmd):
    prompt = '\033[033mDATASHELL/$ \033[00m'

    def preloop(self) -> None:
        preloop.execute()

    def default(self, line: str) -> None:
        get = (line,)
        out = default.execute
        out(get)

    def do_exit(self, _) -> bool:
        out = shexit.execute
        return out()

    def alias(self, args: str) -> None:
        alias.execute()

    def help_alias(self, args: str) -> None:
        pass
