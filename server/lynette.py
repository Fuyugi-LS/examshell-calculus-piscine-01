#!/usr/bin/env python3
# lynette.py — strict runner (redacted .f contents in logs)
from pathlib import Path
import shutil
import subprocess
import shlex
import sys
import hashlib
from typing import Union, List

import questions  # repo-local; returns normal strings per your guarantee

def deepthought() -> str:
    """
    Read and return the full content of the deepthought log file.
    """
    deep_file = Path(__file__).parent / "space" / "deepthought"
    if deep_file.exists():
        return deep_file.read_text(encoding="utf-8")
    else:
        return ""  # return empty string if the file does not exist

ROOT = Path(__file__).parent.resolve()
SPACE = ROOT / "space"
DEEP = SPACE / "deepthought"

# exact flags (do not change)
TEXMAT_FLAGS = ["--strict", "-v", "--to", "object"]
UTEST_FLAGS = ["--prefix", "re", "--sample", "50"]

UTEST_RUNS = 10  # run utest this many times

def ensure_space():
    if SPACE.exists():
        shutil.rmtree(SPACE)
    SPACE.mkdir(parents=True, exist_ok=True)
    DEEP.write_text("", encoding="utf-8")

def log_raw(line: str):
    with DEEP.open("a", encoding="utf-8") as fh:
        fh.write(line + "\n")

def run_and_log(command: Union[List[str], str], shell: bool = False, timeout: int | None = None) -> int:
    """
    Log the exact command (prefixed with $ ), run it, append full stdout+stderr lines, then
    append separator line ========================.
    - If shell=True, command must be a string run under /bin/sh -c.
    - If shell=False, command is a list executed directly.
    Returns the command returncode (or 124/126 for timeout/oserror).
    """
    cmd_display = command if shell else " ".join(shlex.quote(str(x)) for x in command)
    log_raw(f"$ {cmd_display}")
    try:
        if shell:
            proc = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, timeout=timeout)
        else:
            proc = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, timeout=timeout)
        out = proc.stdout or ""
        if out:
            for line in out.rstrip("\n").splitlines():
                log_raw(line)
        log_raw("=======================")
        return proc.returncode
    except subprocess.TimeoutExpired as exc:
        log_raw(f"TIMEOUT: {exc}")
        log_raw("=======================")
        return 124
    except OSError as exc:
        log_raw(f"OSERROR: {exc}")
        log_raw("=======================")
        return 126

def _sha256_hex(s: str) -> str:
    h = hashlib.sha256()
    h.update(s.encode("utf-8"))
    return h.hexdigest()

def write_f_file_redacted(path: Path, text: str):
    """
    Write text to path (UTF-8). But do NOT log content. Instead log:
      - path
      - number of lines
      - byte length
      - sha256 hex of the bytes
    This prevents leaking answers while still providing a checksum for verification.
    """
    path.write_text(text, encoding="utf-8")
    lines = text.count("\n") + (0 if text.endswith("\n") or text == "" else 1)
    bytelen = len(text.encode("utf-8"))
    sha = _sha256_hex(text)
    log_raw(f"# WROTE {path}")
    log_raw(f"# metadata: lines={lines} bytes={bytelen} sha256={sha}")
    log_raw("=======================")

def get_verdict(qid: int, stud_source: str) -> str:
    ensure_space()

    prob_source = questions.get_answer(qid)  # normal string per your guarantee

    sample_f = SPACE / "sample.f"
    user_f = SPACE / "user.f"
    sample_dill = SPACE / "sample.dill"   # expected to be produced by texmat
    user_dill = SPACE / "user.dill"       # expected to be produced by texmat
    res_sample = SPACE / "resample"
    res_user = SPACE / "reuser"

    # 0) Write .f files exactly from strings, but REDACT content in the log
    write_f_file_redacted(sample_f, prob_source)
    write_f_file_redacted(user_f, stud_source)

    # 1) Run texmat with EXACT flags
    texmat_cmd = [str(ROOT / "texmat"), str(sample_f), str(user_f)] + TEXMAT_FLAGS
    tex_rc = run_and_log(texmat_cmd, shell=False, timeout=60)

    # 2) Run utest UTEST_RUNS times; after each run immediately run diff -u resample reuser
    all_utest_ok = True
    all_diffs_ok = True
    for i in range(1, UTEST_RUNS + 1):
        # build utest shell command string (to allow piping to tee -a)
        utest_cmd = f"{shlex.quote(str(ROOT / 'utest'))} {shlex.quote(str(sample_dill))} {shlex.quote(str(user_dill))} {' '.join(shlex.quote(f) for f in UTEST_FLAGS)} | tee -a {shlex.quote(str(DEEP))}"
        log_raw(f"# UTEST RUN {i}/{UTEST_RUNS}")
        utest_rc = run_and_log(utest_cmd, shell=True, timeout=180)
        if utest_rc != 0:
            all_utest_ok = False
        # after this utest run, immediately run diff -u on resample vs reuser (textual diff)
        diff_cmd = ["diff", "-u", str(res_sample), str(res_user)]
        log_raw(f"# DIFF AFTER UTEST RUN {i}/{UTEST_RUNS}")
        diff_rc = run_and_log(diff_cmd, shell=False, timeout=10)
        if diff_rc != 0:
            all_diffs_ok = False
        # continue to next iteration regardless; we log everything

    # 3) After all runs, ensure res files exist and log
    log_raw(f"# RES FILES EXIST: resample={res_sample.exists()}, reuser={res_user.exists()}")
    log_raw("=======================")

    # 4) Final overall diff result appended exactly as requested: final two lines (separator and message)
    log_raw("=========")
    if all_diffs_ok:
        log_raw("diff OK :D")
    else:
        log_raw("diff KO :)")

    # 5) PASS only if all strict conditions met
    if tex_rc == 0 and all_utest_ok and res_sample.exists() and res_user.exists() and all_diffs_ok:
        return "PASS"
    return "FAIL"

if __name__ == "__main__":
    qid = 122
    stud_source = questions.get_answer(122)  # user guarantees normal string
    result = get_verdict(qid, stud_source)
    print(result)
    print("=========================")
    print(deepthought())
