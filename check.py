"""Run solutions and compare their printed answers with <year>/answers.json ({"01": [part1, part2], ...}).

Usage: python check.py [years...] [days...]
  4-digit numbers are years, anything else is a day or range (5, 7-9) applied to every chosen year.
  e.g. check.py            every year, every day
       check.py 2024       all of 2024
       check.py 2024 3 7-9 those days of 2024
       check.py 5          day 5 of every year
Never touches the network: fill answers.json with `python -m utils.api answers <year>`.
"""
lazy import ctypes
import json
import os
import re
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

ROOT = Path(__file__).resolve().parent
PART_RE = re.compile(r"^Part ([12]): (.*?)\s*$", re.M)
TIMEOUT = 300

def _colour_on():
    """Colour only an interactive terminal; cmd/PowerShell consoles need VT processing switched on."""
    if not sys.stdout.isatty():
        return False
    if os.name == "nt":
        k, mode = ctypes.windll.kernel32, ctypes.c_uint32()
        h = k.GetStdHandle(-11)
        # 4 = ENABLE_VIRTUAL_TERMINAL_PROCESSING; best effort, as VS Code and Windows Terminal render ANSI regardless
        if k.GetConsoleMode(h, ctypes.byref(mode)):
            k.SetConsoleMode(h, mode.value | 4)
    return True

def _paint(code):
    return (lambda s: f"\x1b[{code}m{s}\x1b[0m") if COLOUR else str

COLOUR = _colour_on()
# standard green, as some themes render bright green (92) as plain text; bright red stays readable on PowerShell 5's blue
green, red = _paint(32), _paint(91)

def run(year, day, expected):
    """Run one day and return (year, day, status, expected, got)."""
    script = ROOT / year / f"day_{day}" / f"day_{day}.py"
    try:
        r = subprocess.run([sys.executable, script.name], cwd=script.parent, capture_output=True, text=True, timeout=TIMEOUT)
    except subprocess.TimeoutExpired:
        return year, day, "TIMEOUT", expected, None
    found = dict(PART_RE.findall(r.stdout))
    got = [found.get("1"), found.get("2")]
    if r.returncode:
        return year, day, f"ERROR {r.stderr.strip().splitlines()[-1] if r.stderr.strip() else r.returncode}", expected, got
    if expected is None:
        return year, day, "no answer", expected, got
    # a None expected part (e.g. the last day's missing part 2) always passes
    return year, day, "ok" if all(e is None or str(e) == g for e, g in zip(expected, got)) else "FAIL", expected, got

def parse_args(args):
    years, days = [], set()
    for a in args:
        if len(a) == 4 and a.isdigit():
            years.append(a)
        else:
            lo, _, hi = a.partition("-")
            days.update(range(int(lo), int(hi or lo) + 1))
    return years or sorted(p.name for p in ROOT.iterdir() if p.is_dir() and p.name.isdigit()), days

def check(years, days=(), indent=""):
    """Run the chosen solutions in parallel, printing each result in order as it is ready; returns (passed, total)."""
    jobs = []
    for y in map(str, years):
        f = ROOT / y / "answers.json"
        answers = json.loads(f.read_text(encoding="utf-8-sig")) if f.exists() else {}
        for s in sorted((ROOT / y).glob("day_*/day_*.py")):
            d = s.stem[4:]
            if d.isdigit() and (not days or int(d) in days):
                jobs.append((y, d, answers.get(d)))
    n, fails = len(jobs), []
    with ThreadPoolExecutor() as ex:
        for i, (year, day, status, exp, got) in enumerate(ex.map(lambda j: run(*j), jobs), 1):
            detail = "" if status == "ok" else f"  expected {exp}, got {got}" if exp is not None else f"  got {got}"
            line = f"{year} day {day}: {status}{detail}"
            if status != "ok":
                fails.append(line)
            print(f"{indent}{(green if status == 'ok' else red)(f'[{i}/{n}] {line}')}", flush=True)
    print(f"{indent}{(red if fails else green)(f'{n - len(fails)}/{n} passed')}")
    if fails:
        print(f"{indent}{red(f'{len(fails)} failed:')}")
        for line in fails:
            print(f"{indent}  {red(line)}")
    return n - len(fails), n

def main():
    passed, total = check(*parse_args(sys.argv[1:]))
    sys.exit(passed < total)

if __name__ == "__main__":
    main()
