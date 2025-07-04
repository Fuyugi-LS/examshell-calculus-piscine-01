# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
#                                  (      o  )                                #
#                                   \  ‾‾‾  /                                 #
#                                    \_____/                                  #
#                                ─── SciShell ───                             #
#                                                                             #
#    datashell.py                                                             #
#                                                                             #
#    By: Fuyugi <github.com/Fuyugi-LS>                                        #
#                                                                             #
#    Created: 2025/06/29 09:30:00 by Fuyugi                                   #
#    Updated: 2025/07/06 23:00:00 by Fuyugi                                   #
#                                                                             #
#    © CC0 2025                                                               #
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

from utils import stddata


class __SERVICE__:
    pass


def fetch_cmd(name: str) -> str | None:
    out = stddata.shellfetch_json
    return out("datashell", name)

def get_sqlcmd(cmd_name: str = "") -> str | None:
    out = None
    obj = stddata.shellfetch_dict_json("datashell", "sqlcmd")
    if isinstance(obj, dict):
        out = obj["sqlcmd"][cmd_name]
    return out
