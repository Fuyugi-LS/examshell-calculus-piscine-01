# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
#                                  (      o  )                                #
#                                   \  ‾‾‾  /                                 #
#                                    \_____/                                  #
#                                ─── SciShell ───                             #
#                                                                             #
#    pharser.py                                                               #
#                                                                             #
#    By: Fuyugi <github.com/Fuyugi-LS>                                        #
#                                                                             #
#    Created: 2025/06/29 09:30:00 by Fuyugi                                   #
#    Updated: 2025/07/06 23:00:00 by Fuyugi                                   #
#                                                                             #
#    © CC0 2025                                                               #
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

import shlex
from stddb import DataShell
from stddb import alias as method_alias


class alias:
    @staticmethod
    def findeq(input: str) -> int:
        for i in range(0, len(input)):
            if input[i] == '=':
                return i
        raise Exception

    @staticmethod
    def pharser(usrinput: str) -> dict:
        result: dict = {}
        try:
            usrinput = shlex.split(usrinput)
            if len(usrinput) != 1:
                raise Exception
            usrinput = usrinput[0]
            eq = alias.findeq(usrinput)
            result["name"] = usrinput[0:eq]
            result["cmd"] = usrinput[eq+1:]
            return result
        except Exception as _:
            print(DataShell.alias["err"])
            return False

    @staticmethod
    def run_pharser(args: str) -> str:
        """
        replace the indexed zero of the str, by the value in the sqlite alias
        """
        first_args = args.split(" ")[0]
        result = method_alias.select(first_args)
        if result is None:
            raise Exception
        args = args.replace(first_args, result[1])
        return args


class unalias:
    def pharser(usrinput: str) -> dict:
        try:
            usrinput = shlex.split(usrinput)
            if len(usrinput) != 1:
                raise Exception
            return usrinput[0]
        except Exception as _:
            return False
