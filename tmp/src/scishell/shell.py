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
    prompt = '$ '

    def preloop(self) -> None:
        pass

    def default(self, line: str) -> None:
        get = (line,)
        out = default.execute
        out(get)

    def do_exit(self, _) -> bool:
        out = shexit.execute
        return out()

    def do_datashell(self) -> None:
        pass

    def do_examshell(self) -> None:
        pass

    def do_examset(self) -> None:
        pass

    def help_datashell(self) -> None:
        pass

    def help_examshell(self) -> None:
        pass

    def help_examset(self) -> None:
        pass
