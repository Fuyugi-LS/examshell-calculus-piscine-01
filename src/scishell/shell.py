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
from scishell import *


class __MAIN__(cmd.Cmd):
    prompt = '\033[33m$ \033[00m'

    def preloop(self) -> None:
        preloop.execute()

    def default(self, line: str) -> None:
        get = (line,)
        out = default.execute
        out(get)

    def do_exit(self, _) -> bool:
        out = shexit.execute
        return out()

    def do_datashell(self, _) -> None:
        datashell.execute()

    def do_examshell(self, _) -> None:
        examshell.execute()

    def do_examset(self, _) -> None:
        examset.execute()

    def help_datashell(self) -> None:
        pass

    def help_examshell(self) -> None:
        pass

    def help_examset(self) -> None:
        pass
