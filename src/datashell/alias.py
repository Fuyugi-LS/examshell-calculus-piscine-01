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
import re
from shlex import split, quote
from program_file import datashell
from utils.stddata import get_database_connection


class AliasNotFoundError(Exception):
    def __init__(self, alias_name: str):
        self.alias_name = alias_name
        super().__init__(f"Alias '{alias_name}' not found.")


class MultipleMatchesError(Exception):
    def __init__(
            self, matches: list[str],
            message: str = "Multiple commands found that match your input"
            ):
        self.matches = matches
        super().__init__(f"{message}: {', '.join(matches)}")


class __SERVICE__:
    # general_function --------------------------------------------------------
    @staticmethod
    def splitter(get: str) -> str:
        parts = split(get)
        for i in range(0, len(parts)):
            par = parts[i]
            if not (
                re.search(r'^["|\']', par)
                or re.search(r'["|\']$', par)
                    ):
                parts[i] = "'" + par + "'"
        return ' '.join(parts)

    @staticmethod
    def noop(*args: Any, **kwargs: Any) -> Tuple[Any, ...]:
        return ()

    @staticmethod
    def runner(operation: str, activate_function:
               Callable[..., Any] = noop,
               parameters: Tuple[Any, ...] = ()
               ) -> Optional[list[tuple[Any, ...]]]:
        a = activate_function
        db = get_database_connection()
        out: Optional[list[tuple[Any, ...]]] = None
        try:
            rem = db.cursor()
            cmd = datashell.get_sqlcmd('alias', operation)
            if cmd is None:
                raise ValueError()
            fill = a(*parameters)
            rem.execute(cmd, fill)
            if (operation == 'select'):
                out = rem.fetchall()
            db.commit()
        except Exception as e:
            raise e
        finally:
            db.close()
        return out
    # eohf --------------------------------------------------------------------
    # gen_alias ---------------------------------------------------------------

    @staticmethod
    def get_default(parsed_args: list[Any],
                    syscmd: bool = False) -> tuple[Any, ...]:
        if " " in parsed_args[0]:
            raise ValueError("Forbidden control structure")
        parsed_args[0] = __SERVICE__.splitter(parsed_args[0])
        out = (parsed_args[0], parsed_args[1], 'default', 0, 0,
               syscmd)
        return out

    @staticmethod
    def get_params(parsed_args: list[Any],
                   isiterate: bool, syscmd: bool = False) -> tuple[Any, ...]:
        isorder = False
        if parsed_args[0] == '@o':
            isorder = True
        if " " in parsed_args[1]:
            raise ValueError("Forbidden control structure")
        parsed_args[1] = __SERVICE__.splitter(parsed_args[1])
        out = (parsed_args[1], parsed_args[2], 'parameter', isorder, isiterate,
               syscmd)
        return out

    @staticmethod
    def get_reformat(parsed_args: list[Any],
                     isiterate: bool, syscmd: bool = False) -> tuple[Any, ...]:
        isorder = False
        if parsed_args[0] == '@o':
            isorder = True
        if "??" in parsed_args[1]:
            raise ValueError("Forbidden control structure")
        parsed_args[1] = __SERVICE__.splitter(parsed_args[1])
        out = (parsed_args[1], parsed_args[2], 'reformat', isorder, isiterate,
               syscmd)
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
            if get[1][-1] == 'd' and get[1][0] == '-':
                raise ValueError()
            if not get[1] in flags:
                get = get[:1] + ['--default',] + get[1:]
            if len(get[1]) < 3 and not get[2] in extra_order_flags:
                get[1] = "{}d".format(get[1])
            elif len(get[1]) < 3 and get[2] in extra_order_flags:
                get[1] = "{}o".format(get[1])
                get = get[:2] + get[3:]
            elif (len(get[1]) > 3
                  and get[1][0] == '-'
                  and get[1] != '--default'
                  and get[2] in extra_order_flags):
                get = get[:2] + ['@o'] + get[3:]
            elif (len(get[1]) > 3
                  and get[1][0] == '-'
                  and get[1] != '--default'
                  and not get[2] in extra_order_flags
                  and not get[2][0] == '-'):
                get = get[:2] + ['@d'] + get[2:]
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
            out = parse.parse_args(get[1:])
        except (ValueError, SystemExit) as _:
            out = None
        finally:
            return out

    @staticmethod
    def checkiterate(ch: str) -> tuple[str, Optional[bool]]:
        flags = ('-p', '-r', '-po', '-ro', '--parameter', '--reformat')
        out: tuple[str, Optional[bool]] = ("", None)
        get = split(ch)
        isiterate = "-i" == get[0] or '--iterate' == get[0]
        if isiterate:
            nmsg = get[1:]
            dmsg = map(quote, nmsg)
            msg = " ".join(dmsg)
            out = (msg, isiterate)
        elif (not get[0] in flags) and get[0][0] == '-':
            raise ValueError()
        else:
            out = (ch, isiterate)
        return out
    # eohf --------------------------------------------------------------------
    # use_alias ---------------------------------------------------------------

    @staticmethod
    def __select_query(name: str) -> str:
        return name

    @staticmethod
    def __get_matcmd__(argv: str) -> list[tuple[Any, ...]]:
        query = split(argv)[0]
        val = __SERVICE__.runner("select",
                                 __SERVICE__.__select_query, (query,))
        if val is None:
            raise ValueError("cannot fetch query")
        return val

    @staticmethod
    def get_matcmd_str(argv: list[str]) -> tuple[str, ...]:
        return (argv[0],)

    @staticmethod
    def _hf_sort_data_(msg: tuple[Any, ...]) -> int:
        out = -1
        if msg[2] == 'reformat':
            out = 1
        else:
            out = 2
        return out

    @staticmethod
    def select_bestcmd(candidates: list[tuple[Any, ...]],
                       argv: str) -> tuple[Any, ...]:
        out: tuple[Any, ...] | None = None
        candidates = sorted(candidates, key=__SERVICE__._hf_sort_data_)
        for candidate in candidates:
            if candidate[2] == 'reformat':
                verdict = False
                tcmds = re.split(r'\?\d*', candidate[0])
                cmds: list[str] = []
                for tc in tcmds:
                    max = len(tc) - 1
                    ttc = tc[1:max]
                    if tc and ttc.strip() != "":
                        cmds.append(tc)
                # stnd = (re.findall(rf'^{re.escape(cmds[0])}', rf'{argv}')
                #         and re.findall(rf'{re.escape(cmds[len(cmds) - 1])}$',
                # rf'{argv}'))
                # if not stnd:
                #     # continue
                orc = 0
                tmp = argv
                mem = True
                for i in range(0, len(cmds)):
                    cs = cmds[i]
                    if cs in tmp:
                        seq = tmp.find(cs) + len(cs)
                        tmp = tmp[seq:]
                        orc += 1
                    else:
                        mem = False
                        break
                if mem is False:
                    continue
                mem = True
                verdict = mem
                if verdict:
                    out = candidate
                    break
            else:
                sample = candidate[0]
                if sample == re.split(r' ', argv)[0]:
                    out = candidate
                    break
        if out is None:
            raise SystemError("Not possible out variable None type error")
        return out

    @staticmethod
    def fetchcmd(argv: str) -> str:
        out: str = "__SYS__STDERR__"
        fun = __SERVICE__.get_matcmd_str
        argv = __SERVICE__.splitter(argv)
        cmlist = __SERVICE__.runner('select', fun, (re.split(r' ', argv),))
        if cmlist == [] or cmlist is None:
            raise AliasNotFoundError(argv)
        cmdlist: list[tuple[Any, ...]] = []
        for i in range(0, len(cmlist)):
            cur = list(cmlist[i])
            cur[0] = __SERVICE__.splitter(cur[0])
            cmdlist.append(tuple(cur))
        best = __SERVICE__.select_bestcmd(cmdlist, argv)
        out = best[0]
        return out
    # eohf --------------------------------------------------------------------


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


def _create() -> None:
    try:
        __SERVICE__.runner('gen')
    except Exception as e:
        print(e)
        raise SystemError('Not possible create alias error')


def create_alias(ch: str, sysalias: bool = False) -> None:
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
                               (get['default'], sysalias))
        elif get["parameter"]:
            alias_name = get['parameter'][1]
            cmd = get['parameter'][2]
            __SERVICE__.runner('insert', __SERVICE__.get_params,
                               (get['parameter'], isindex, sysalias))
        elif get["reformat"]:
            alias_name = get['reformat'][1]
            cmd = get['reformat'][2]
            __SERVICE__.runner('insert', __SERVICE__.get_reformat,
                               (get['reformat'], isindex, sysalias))
        msg = datashell.get_output('alias', 'success')
        if isinstance(msg, str):
            print(msg.format(alias_name, cmd))
    except Exception as _:
        print(datashell.get_output('alias', 'err'))
    finally:
        return


def use_alias(argv: str) -> None:
    print(__SERVICE__.fetchcmd(argv))
