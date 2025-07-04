# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
#                                  (      o  )                                #
#                                   \  ‾‾‾  /                                 #
#                                    \_____/                                  #
#                                ─── SciShell ───                             #
#                                                                             #
#    stddata.py                                                               #
#                                                                             #
#    By: Fuyugi <github.com/Fuyugi-LS>                                        #
#                                                                             #
#    Created: 2025/06/29 09:30:00 by Fuyugi                                   #
#    Updated: 2025/07/06 23:00:00 by Fuyugi                                   #
#                                                                             #
#    © CC0 2025                                                               #
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

import json
from typing import Optional, TextIO
from utils import path


class __SERVICE__:
    pass


def shellfetch_json(filename: str, name: str) -> str | None:
    out = None
    f: Optional[TextIO] = None
    try:
        f = open(path.program_file(isglobal=False) + filename +
                 '.json', 'r', encoding='utf-8')
        tmp = json.load(f)
        out = tmp[name]
    except Exception as e:
        print(e)
    finally:
        if f is not None:
            f.close()
        return out
