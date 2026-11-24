"""Re-run <year>/day_XX/day_XX.py and compare the printed answers with <year>/answers.json ({"01": [part1, part2], ...}).

Usage: python check.py [years...]   (default: every year folder)
"""
import json
import re
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

ROOT = Path(__file__).resolve().parent
PART_RE = re.compile(r"^Part ([12]): (.*?)\s*$", re.M)


def run(year, day, expected):
    """Run <year>/day_<day>/day_<day>.py and return (year, day, passed, expected, got)."""
    script = ROOT / year / f"day_{day}" / f"day_{day}.py"
    r = subprocess.run([sys.executable, script.name], cwd=script.parent, capture_output=True, text=True)
    found = dict(PART_RE.findall(r.stdout))
    got = [found.get("1"), found.get("2")]
    return year, day, all(e is None or str(e) == g for e, g in zip(expected, got)), expected, got


def main():
    """Check every requested year in parallel and exit non-zero if any day fails."""
    years = sys.argv[1:] or sorted(p.name for p in ROOT.iterdir() if p.is_dir() and p.name.isdigit())
    jobs = [(y, d, exp) for y in years if (f := ROOT / y / "answers.json").exists()
            for d, exp in sorted(json.loads(f.read_text(encoding="utf-8-sig")).items())]
    with ThreadPoolExecutor() as ex:
        results = list(ex.map(lambda j: run(*j), jobs))
    for year, day, ok, exp, got in results:
        print(f"{year} day {day}: " + ("ok" if ok else f"FAIL expected {exp}, got {got}"))
    fails = sum(not r[2] for r in results)
    print(f"{len(results) - fails}/{len(results)} passed")
    sys.exit(fails > 0)


if __name__ == "__main__":
    main()
