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
import datashell.pharser as pharser
from stddb import DataShell as Data
from stddb import alias as method_alias


class DataShell(cmd.Cmd):
    prompt = "[DATA]$ "

    def preloop(self):
        print(Data().introduction)

    def do_exit(self, _):
        print(Data().exit)
        return True

    def default(self, line):
        try:
            self.onecmd(pharser.alias.run_pharser(line))
        except Exception as _:
            print(f"Unknown command: '{line}'")

    def do_alias(self, args):
        args = pharser.alias.pharser(args)
        if (args is False
            or len(args["name"].strip()) == 0
                or len(args["cmd"].strip()) == 0):
            print(Data.alias["err"])
            return
        method_alias.insert(args)
        print((Data.alias["success"]).format
              (args["name"].strip(), args["cmd"].strip()))

    def do_unalias(self, args):
        args = pharser.unalias.pharser(args)
        try:
            if args is False or len(args) == 0:
                raise Exception
            method_alias.delete(args)
            print(Data.unalias["success"].format(args))
        except Exception as _:
            print(Data.unalias["err"])

    def do_dataset(self, args):
        pass

    def do_dataset(self, args):
        pass

    def do_rm(self, args):
        pass

    def do_ls(self, args):
        pass

    def do_open(self, args):
        pass

    def do_edit(self, args):
        pass

    def do_close(self, args):
        pass

    def do_touch(self, args):
        pass

    def do_examset(self, args):
        pass
