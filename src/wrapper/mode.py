# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
#                                  (      o  )                                #
#                                   \  ‾‾‾  /                                 #
#                                    \_____/                                  #
#                                ─── SciShell ───                             #
#                                                                             #
#    mode.py                                                                  #
#                                                                             #
#    By: Fuyugi <github.com/Fuyugi-LS>                                        #
#                                                                             #
#    Created: 2025/06/29 09:30:00 by Fuyugi                                   #
#    Updated: 2025/07/06 23:00:00 by Fuyugi                                   #
#                                                                             #
#    © CC0 2025                                                               #
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

import cmd
from stddb import Wrapper
from shlex import split
from datashell.shell import DataShell


class InitMode(cmd.Cmd):
    prompt = '$ '

    def preloop(self):
        print(Wrapper().introduction)

    def default(self, line):
        print(f"Unknown command: '{line}'")

    def do_datashell(self, _):
        DataShell().cmdloop()

    def do_examshell(self, _):
        print("Buzz")

    def do_exit(self, _):
        print(Wrapper.exit)
        return True

    def help_datashell(self):
        pass

    def help_examshell(self):
        pass
