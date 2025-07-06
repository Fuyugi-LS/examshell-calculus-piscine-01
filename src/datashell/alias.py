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
import argparse
from shlex import split, quote
from program_file import datashell
from utils.stddata import get_database_connection


class __SERVICE__:
    @staticmethod
    def noop(*args: Any, **kwargs: Any) -> Tuple[Any, ...]:
        return ()

    @staticmethod
    def runner(operation: str, activate_function:
               Callable[..., Any] = noop,
               parameters: Tuple[Any, ...] = ()) -> None:
        a = activate_function
        db = get_database_connection()
        try:
            rem = db.cursor()
            cmd = datashell.get_sqlcmd('alias', operation)
            if cmd is None:
                raise ValueError()
            fill = a(*parameters)
            rem.execute(cmd, fill)
            db.commit()
        except Exception as e:
            raise e
        finally:
            db.close()

    @staticmethod
    def get_default(parsed_args: list[Any]) -> tuple[Any, ...]:
        out = (parsed_args[0], parsed_args[1], 'default', 0, 0)
        return out

    @staticmethod
    def get_params(parsed_args: list[Any], isiterate: bool) -> tuple[Any, ...]:
        isorder = False
        if parsed_args[0] == '@o':
            isorder = True
        out = (parsed_args[1], parsed_args[2], 'parameter', isorder, isiterate)
        return out

    @staticmethod
    def get_reformat(parsed_args: list[Any],
                     isiterate: bool) -> tuple[Any, ...]:
        isorder = False
        if parsed_args[0] == '-o' or parsed_args[0] == '--order':
            isorder = True
        out = (parsed_args[1], parsed_args[2], 'reformat', isorder, isiterate)
        return out

    @staticmethod
    def parser(args: str) -> Optional[argparse.Namespace]:
        out: Optional[argparse.Namespace] = None
        try:
            flags = ('-p', '-r', '-po', '-ro', '--parameter', '--reformat')
            extra_order_flags = ('-o', '--order')
            get = split(args)
            if len(get) < 3:
                raise ValueError()
            if get[1][-1] == 'd':
                raise ValueError()
            if not get[1] in flags:
                get = get[:1] + ['--default',] + get[1:]
            if len(get[1]) < 3 and not get[2] in extra_order_flags:
                get[1] = "{}d".format(get[1])
            elif len(get[1]) < 3 and get[2] in extra_order_flags:
                get[1] = "{}o".format(get[1])
                get = get[:2] + get[3:]
            elif len(get[1]) >= 3 and get[1][0] == '-' and get[1] != '--default' and get[2] in extra_order_flags:
                get = get[:2] + ['@o'] + get[3:]
            elif len(get[1]) >= 3 and get[1][0] == '-' and get[1] != '--default' and not get[2] in extra_order_flags and get[2][0] == '-':
                get = get[:2] + ['@d'] + get[2:]
            print(get)
            if len(get[1]) == 3:
                get = get[:1] + [get[1][:2]] + ['@' + get[1]
                                                         [2]] + get[2:]
            parse = argparse.ArgumentParser(
                prog='cmd',
                add_help=False
            )
            parse.add_argument('--default', nargs=2, default=[])
            parse.add_argument('-p', '--parameter', nargs=3, default=[])
            parse.add_argument('-r', '--reformat', nargs=3, default=[])
            print(get[1:])
            out = parse.parse_args(get[1:])
        except (ValueError, SystemExit) as e:
            print(e)
            out = None
        finally:
            return out

    @staticmethod
    def checkiterate(ch: str) -> tuple[str, Optional[bool]]:
        out: tuple[str, Optional[bool]] = ("", None)
        get = split(ch)
        isiterate = "-i" in get[0] or '--iterate' in get[0]
        if isiterate:
            nmsg = get[1:]
            dmsg = map(quote, nmsg)
            msg = " ".join(dmsg)
            out = (msg, isiterate)
        else:
            out = (ch, isiterate)
        return out


def _foreparse(ch: str) -> Optional[dict[Any, Any]]:
    out: Optional[dict[Any, Any]] = None
    try:
        io = __SERVICE__.parser(ch)
        if io is not None:
            out = vars(io)
        else:
            raise ValueError()
    except ValueError as _:
        raise ValueError()
    finally:
        return out


def _create() -> None:  # type: ignore
    try:
        __SERVICE__.runner('gen')
    except Exception as e:
        print(e)
        raise SystemError('Not possible create alias error')


def create_alias(ch: str) -> None:
    _create()
    try:
        isindex = __SERVICE__.checkiterate(ch)[1]
        ch = quote("cmd") + ' ' + __SERVICE__.checkiterate(ch)[0]
        get = _foreparse(ch)
        alias_name: Optional[str] = None
        cmd: Optional[str] = None
        if get is None:
            raise ValueError()
        if get["default"]:
            alias_name = get['default'][0]
            cmd = get['default'][1]
            __SERVICE__.runner('insert', __SERVICE__.get_default,
                               (get['default'],))
        elif get["parameter"]:
            alias_name = get['parameter'][1]
            cmd = get['parameter'][2]
            __SERVICE__.runner('insert', __SERVICE__.get_params,
                               (get['parameter'], isindex))
        elif get["reformat"]:
            alias_name = get['reformat'][1]
            cmd = get['reformat'][2]
            __SERVICE__.runner('insert', __SERVICE__.get_reformat,
                               (get['reformat'], isindex))
        msg = datashell.get_output('alias', 'success')
        if isinstance(msg, str):
            print(msg.format(cmd, alias_name))
    except Exception as _:
        print(datashell.get_output('alias', 'err'))
    finally:
        return
