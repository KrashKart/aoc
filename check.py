"""Run solutions and compare their printed answers with <year>/answers.json ({"01": [part1, part2], ...}).

Usage: python check.py [years...] [days...]
  4-digit numbers are years, anything else is a day or range (5, 7-9) applied to every chosen year.
  e.g. check.py            every year, every day
       check.py 2024       all of 2024
       check.py 2024 3 7-9 those days of 2024
       check.py 5          day 5 of every year
Never touches the network: fill answers.json with `python -m utils.api answers <year>`.
"""
import json
import re
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

ROOT = Path(__file__).resolve().parent
PART_RE = re.compile(r"^Part ([12]): (.*?)\s*$", re.M)
TIMEOUT = 300

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

def main():
    years, days = parse_args(sys.argv[1:])
    jobs = []
    for y in years:
        f = ROOT / y / "answers.json"
        answers = json.loads(f.read_text(encoding="utf-8-sig")) if f.exists() else {}
        for s in sorted((ROOT / y).glob("day_*/day_*.py")):
            d = s.stem[4:]
            if d.isdigit() and (not days or int(d) in days):
                jobs.append((y, d, answers.get(d)))
    with ThreadPoolExecutor() as ex:
        results = list(ex.map(lambda j: run(*j), jobs))
    for year, day, status, exp, got in results:
        detail = "" if status == "ok" else f"  expected {exp}, got {got}" if exp is not None else f"  got {got}"
        print(f"{year} day {day}: {status}{detail}")
    passed = sum(r[2] == "ok" for r in results)
    print(f"{passed}/{len(results)} passed")
    sys.exit(passed < len(results))

if __name__ == "__main__":
    main()
