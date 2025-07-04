# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
#                                  (      o  )                                #
#                                   \  ‾‾‾  /                                 #
#                                    \_____/                                  #
#                                ─── SciShell ───                             #
#                                                                             #
#    alias.py                                                                 #
#                                                                             #
#    By: Fuyugi <github.com/Fuyugi-LS>                                        #
#                                                                             #
#    Created: 2025/06/29 09:30:00 by Fuyugi                                   #
#    Updated: 2025/07/06 23:00:00 by Fuyugi                                   #
#                                                                             #
#    © CC0 2025                                                               #
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

from typing import Callable, Optional, Any, Tuple
from program_file import datashell
from utils.stddata import get_database_connection


class __SERVICE__:
    @staticmethod
    def runner(activate_function: Callable[..., Any],
               parameters: Tuple[Any, ...] = ()) -> None:
        a = activate_function
        db = get_database_connection()
        try:
            rem = db.cursor()
            rem.execute(a(*parameters))
            db.commit()
        except Exception as _:
            raise ValueError()
        finally:
            db.close()

    @staticmethod
    def alias_data(cmd: str) -> Optional[str]:
        out = datashell.get_sqlcmd('alias', cmd)
        return out


def _create() -> None:  # type: ignore
    try:
        racing = __SERVICE__.alias_data
        __SERVICE__.runner(racing, ('gen',))
    except Exception as _:
        raise SystemError('Not possible create alias error')


def execute() -> None:
    pass
