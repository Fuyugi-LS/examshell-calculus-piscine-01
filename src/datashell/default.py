# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
#                                  (      o  )                                #
#                                   \  ‾‾‾  /                                 #
#                                    \_____/                                  #
#                                ─── SciShell ───                             #
#                                                                             #
#    default.py                                                               #
#                                                                             #
#    By: Fuyugi <github.com/Fuyugi-LS>                                        #
#                                                                             #
#    Created: 2025/06/29 09:30:00 by Fuyugi                                   #
#    Updated: 2025/07/06 23:00:00 by Fuyugi                                   #
#                                                                             #
#    © CC0 2025                                                               #
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

from program_file import datashell
from datashell.alias import use_alias


class __SERVICE__:
    pass


def execute(get: tuple[str]) -> None:
    out = datashell.fetch_cmd("not_found")
    try:
        use_alias(*get)
    except Exception as _:
        if isinstance(out, str):
            val = get[0]
            val = val.split()[0]
            out = out.format(val)
            print(out)
        else:
            raise SystemError("Not possible string tuple.")
    finally:
        return None
