#!/usr/bin/env python3
"""
utest.py

Usage:
    utest.py sample.dill user.dill [--sample-count N] [--prefix PREFIX] [--seed S] [--outdir DIR]

Produces two output files: {prefix}sample and {prefix}user with one line per test.
Each line is repr(result) or "ERROR: <message>" if the call failed.

Example:
    python utest.py space/sample.dill space/user.dill --sample-count 50 --prefix re
"""

from pathlib import Path
import argparse
import dill # type: ignore
import inspect
import numpy as np # type: ignore
import random
import sys
import traceback

def load_callable(path: Path):
    with open(path, "rb") as f:
        obj = dill.load(f)
    if not callable(obj):
        raise TypeError(f"Loaded object from {path} is not callable.")
    return obj

def try_call(func, args, try_array_if_scalar=True):
    """
    Try calling func(*args).
    If TypeError or specific call problems and try_array_if_scalar is True,
    try converting scalar args to numpy arrays (1-element) and call again.
    Returns (ok: bool, result_or_exception_str)
    """
    try:
        r = func(*args)
        return True, r
    except TypeError as e:
        # maybe needs array instead of scalar
        if try_array_if_scalar and len(args) == 1:
            try:
                arr = np.array([args[0]])
                r = func(arr)
                return True, r
            except Exception as e2:
                return False, f"ERROR TypeError then array attempt failed: {e2}"
        return False, f"ERROR TypeError: {e}"
    except Exception as e:
        # runtime error
        tb = traceback.format_exc()
        return False, f"ERROR Exception: {e}\n{tb}"

def determine_arity(func):
    """
    Use inspect.signature to determine number of positional-or-keyword parameters.
    If signature not available, fallback to 1 (best-effort).
    """
    try:
        sig = inspect.signature(func)
        params = [p for p in sig.parameters.values()
                  if p.kind in (p.POSITIONAL_ONLY, p.POSITIONAL_OR_KEYWORD)]
        return len(params)
    except Exception:
        return 1

def main():
    p = argparse.ArgumentParser(description="Run randomized utest for sample.dill and user.dill")
    p.add_argument("sample", type=Path, help="path to sample .dill")
    p.add_argument("user", type=Path, help="path to user .dill")
    p.add_argument("--sample-count", "-n", dest="count", type=int, default=50, help="number of random tests")
    p.add_argument("--prefix", "-p", dest="prefix", default="re", help="output prefix (default 're')")
    p.add_argument("--seed", type=int, default=None, help="random seed (optional)")
    p.add_argument("--outdir", type=Path, default=Path("."), help="directory to write outputs (override auto)")
    args = p.parse_args()

    sample_path = args.sample
    user_path = args.user
    count = args.count
    prefix = args.prefix
    seed = args.seed
    outdir_arg = args.outdir

    # load callables (fail early if load fails)
    try:
        sample_fn = load_callable(sample_path)
    except Exception as e:
        print(f"Failed to load sample callable from {sample_path}: {e}", file=sys.stderr)
        sys.exit(2)

    try:
        user_fn = load_callable(user_path)
    except Exception as e:
        print(f"Failed to load user callable from {user_path}: {e}", file=sys.stderr)
        sys.exit(3)

    # decide outdir:
    # - if user passed --outdir (not default '.'), use it
    # - else use sample_path.parent (so outputs go to same folder as sample.dill, e.g. Space)
    # - if that parent somehow doesn't exist, fallback to "./Space"
    if outdir_arg != Path("."):
        outdir = Path(outdir_arg)
    else:
        # prefer sample parent if available
        parent = sample_path.parent
        if parent != Path(".") and parent.exists():
            outdir = parent
        else:
            outdir = Path("Space")
    outdir.mkdir(parents=True, exist_ok=True)

    # reproducible RNG
    if seed is None:
        seed = random.randrange(2**31)
    rng = random.Random(seed)

    # determine arities
    sample_arity = determine_arity(sample_fn)
    user_arity = determine_arity(user_fn)

    # Use the larger arity to generate args consistently, but when calling lower-arity func,
    # only pass the needed prefix of args.
    max_arity = max(sample_arity, user_arity)

    out_sample = outdir / f"{prefix}sample"
    out_user = outdir / f"{prefix}user"

    with open(out_sample, "w", encoding="utf-8") as fs, open(out_user, "w", encoding="utf-8") as fu:
        for i in range(count):
            # create args for max_arity (floats in [-10,10])
            args_tuple = tuple(float(rng.uniform(-10, 10)) for _ in range(max_arity))

            # call sample: use its arity
            sample_args = args_tuple[:sample_arity]
            ok_s, res_s = try_call(sample_fn, sample_args, try_array_if_scalar=True)

            # call user: use its arity (same seed/args portion)
            user_args = args_tuple[:user_arity]
            ok_u, res_u = try_call(user_fn, user_args, try_array_if_scalar=True)

            # write lines: use repr for deterministic textual form
            def fmt(x):
                if isinstance(x, str) and x.startswith("ERROR"):
                    return x
                try:
                    # try to convert numpy arrays -> list for nicer repr
                    if hasattr(x, "tolist"):
                        try:
                            return repr(x.tolist()) # type: ignore
                        except Exception:
                            pass
                    return repr(x)
                except Exception:
                    return repr(str(x))

            line_s = fmt(res_s)
            line_u = fmt(res_u)

            fs.write(line_s + "\n")
            fu.write(line_u + "\n")

    print(f"Wrote {count} results to {out_sample} and {out_user} (seed={seed})")
    # exit 0 even if some calls were errors; caller can diff files to detect mismatch.
    return 0

if __name__ == "__main__":
    sys.exit(main())
