# make_callable_and_dump.py
import sympy # type: ignore
from sympy import sympify, lambdify # type: ignore
try:
    from sympy.parsing.latex import parse_latex # type: ignore
    HAVE_PARSE_LATEX = True
except Exception:
    HAVE_PARSE_LATEX = False

import dill # type: ignore
from pathlib import Path
import textwrap

def _parse_expr_from_text(txt):
    txt = txt.strip()
    # try plain sympy parsing first
    try:
        expr = sympify(txt)
        return expr
    except Exception:
        pass
    # fallback: try parse_latex if available
    if HAVE_PARSE_LATEX:
        try:
            expr = parse_latex(txt) # type: ignore
            return expr
        except Exception:
            pass
    raise ValueError("Could not parse expression (not plain sympy or latex).")

def _make_callable_from_expr(expr):
    syms = sorted(expr.free_symbols, key=lambda s: s.name)
    if len(syms) == 0:
        # constant expression -> return zero-arg callable
        const_val = float(expr.evalf())
        return lambda *args, **kwargs: const_val
    # create numpy-aware function; deterministic arg order by symbol name
    f = lambdify(syms, expr, modules=['numpy'])
    if len(syms) == 1:
        # single-arg wrapper: accept float/array
        def wrapper(x): # type: ignore
            return f(x)
        return wrapper
    else:
        # multi-arg wrapper (positional)
        def wrapper(*args):
            return f(*args)
        return wrapper

def _load_function_from_def_text(txt, func_name=None):
    """
    Exec the text in a fresh namespace and return a function object.
    If func_name provided, return that name; else return first callable found.
    WARNING: exec() is unsafe on untrusted input.
    """
    ns = {}
    exec(textwrap.dedent(txt), ns)
    if func_name:
        obj = ns.get(func_name)
        if callable(obj):
            return obj
        raise ValueError(f"Function named {func_name!r} not found in provided code.")
    # otherwise find first callable excluding builtins
    for k, v in ns.items():
        if callable(v) and k != "__builtins__":
            return v
    raise ValueError("No callable found in provided code.")

def make_callable_and_dump(sample_file, user_file, out_dir="Space", strict=False, verbose=False, to="object"):
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    def process_one(path, basename):
        txt = Path(path).read_text(encoding="utf8").strip()
        # heuristics: if file contains "def " or "lambda" treat as python function
        if "def " in txt or txt.startswith("lambda") or "->" in txt:
            if verbose: print(f"[parse] treating {path} as python def/lambda")
            func = _load_function_from_def_text(txt)
        else:
            # treat as expression (try sympy)
            if verbose: print(f"[parse] treating {path} as sympy expression")
            expr = _parse_expr_from_text(txt)
            func = _make_callable_from_expr(expr)
        # optional strict: may wrap to force scalar output shape, etc.
        outpath = out_dir / f"{basename}.dill"
        with open(outpath, "wb") as f:
            dill.dump(func, f)
        if verbose: print(f"[dump] wrote callable to {outpath}")
        return outpath

    sample_out = process_one(sample_file, "sample")
    user_out = process_one(user_file, "user")
    # print final locations (utest can read these)
    print(str(sample_out))
    print(str(user_out))
    return sample_out, user_out

# CLI shim for quick manual runs
if __name__ == "__main__":
    import fire # type: ignore
    fire.Fire(make_callable_and_dump)
