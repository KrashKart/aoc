"""Update everything: inputs (scaffolding new days from day_template.py), answers.json, README badges + charts, check.py.

Usage: python update.py [years...] [--no-check]
  years limit the input/answer fetches and the check (default: every unlocked year); the README always shows every year.
"""
from check import check
from utils.api import days_in, fetch_answers, fetch_input, input_path, unlocked
from utils.core import ROOT
from utils.progress import all_years, update_readme
import shutil
import sys
import time

def stage(n, total, name):
    print(f"\n[{n}/{total}] {name}", flush=True)

def inputs(year):
    """Fetch missing inputs and create day_XX.py from the template where absent."""
    days, fetched = [d for d in range(1, days_in(year) + 1) if unlocked(year, d)], 0
    for d in days:
        f = input_path(d, year)
        # older days may keep their input under other names (e.g. 2023 day 8's nodes.txt)
        if not (f.exists() and f.stat().st_size or any(not p.name.startswith("test") for p in f.parent.glob("*.txt"))):
            print(f"  {year} day {d:02}: fetching input", flush=True)
            fetch_input(d, year)
            fetched += 1
        if not (py := f.with_suffix(".py")).exists():
            shutil.copyfile(ROOT / "day_template.py", py)
            print(f"  {year} day {d:02}: created {py.relative_to(ROOT)}", flush=True)
    print(f"  {year}: {len(days)} days unlocked, {fetched} inputs fetched", flush=True)

def answers(year):
    ans = fetch_answers(year, on_fetch=lambda d: print(f"  {year} day {d:02}: fetching answers", flush=True))
    print(f"  {year}: {sum(a is not None for v in ans.values() for a in v)} answers known", flush=True)

def main():
    args = [a for a in sys.argv[1:] if a != "--no-check"]
    run_check = len(args) == len(sys.argv) - 1
    years = [y for y in map(int, args) if unlocked(y, 1)] if args else all_years()
    if not years:
        sys.exit("no unlocked years to update")
    total, t = 4 if run_check else 3, time.perf_counter()
    try:
        stage(1, total, "Inputs")
        for y in years:
            inputs(y)
        stage(2, total, "Answers")
        for y in years:
            answers(y)
        stage(3, total, "README badges + charts")
        update_readme()
    except RuntimeError as e:
        sys.exit(str(e))
    passed = n = 0
    if run_check:
        stage(4, total, "Check")
        passed, n = check(years, indent="  ")
    print(f"\nDone in {time.perf_counter() - t:.1f}s")
    sys.exit(passed < n)

if __name__ == "__main__":
    main()
