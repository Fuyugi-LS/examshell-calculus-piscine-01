# ExamShell Server

This repository contains the server-side infrastructure for running, testing, and grading symbolic computation exercises using LaTeX (`.f`) inputs, the `texmat` compiler, and the `utest` grader.

## Project Structure

```

server/
├── lynette.py         # Main script to setup, compile, run tests, and log outputs
├── questions.py       # Question definitions and reference answers
├── texmat             # Custom LaTeX compiler
├── utest              # Grader for serialized callables
├── space/             # Temporary working directory
│   ├── sample.f       # Sample input LaTeX
│   ├── user.f         # User input LaTeX
│   ├── sample.dill    # Compiled callable from sample.f
│   ├── user.dill      # Compiled callable from user.f
│   ├── resample       # utest output from sample.dill
│   ├── reuser         # utest output from user.dill
│   └── deepthought    # Logs of all commands and outputs
├── utils/             # Utility modules for texmat and utest
└── requirements.txt

````

Other project directories:  

- `usrspace/` — auxiliary scripts and user-space utilities.
- `hiworld/` — example or temporary files.

## Setup

1. Create a virtual environment:

```bash
python -m venv .venv
source .venv/bin/activate
````

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Ensure `texmat` and `utest` are executable:

```bash
chmod +x texmat utest
```

## Usage

Run the main grading script:

```bash
python lynette.py
```

This performs the following steps:

1. Writes `.f` files for the sample and user exercises.
2. Compiles `.f` files with `texmat` → generates `.dill` callables.
3. Runs `utest` on `.dill` callables → generates `resample` and `reuser`.
4. Logs **all commands and outputs** to `space/deepthought`.
5. Optionally, compares outputs (via `diff` or by deserializing `.dill` callables).

### Notes

* `.dill` files are **binary serialized callables** — do not manually edit.
* `diff` on `.dill` is **not meaningful**; check correctness via `utest` outputs.
* `space/` is fully disposable; all temporary files are regenerated each run.

## Logging

All commands (success or fail) and outputs are appended to:

```
space/deepthought
```

This includes:

* `texmat` compilation logs
* `utest` run logs
* Optional diff results

## Git

Recommended `.gitignore`:

* Ignore `.pyc`, `.dill`, logs, `__pycache__`, virtual environments, and `space` outputs.
* Track only source `.py` and `.f` files.

## License

Now working on license, update later
