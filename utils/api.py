"""Polite Advent of Code client: puzzle inputs, personal stats and leaderboard times.

Every request names a contact in its User-Agent, requests are throttled, 
inputs are downloaded once and kept, nothing is requested before it unlocks, and leaderboard /
stats pages are reused for at least 15 minutes.

CLI: python -m utils.api input <year> [days...]     days like 9 13-25, default all
     python -m utils.api answers <year> [days...]   fills <year>/answers.json for check.py
     python -m utils.api stats <year>
     python -m utils.api cutoffs <year>
"""
import json
import os
import re
import sys
import time
from datetime import datetime, timedelta, timezone
from html import unescape
from math import inf
from urllib.error import HTTPError
from urllib.request import Request, urlopen
from .core import ROOT, infer_day, infer_year, input_path

BASE = "https://adventofcode.com"
CACHE = ROOT / ".cache"
EST = timezone(timedelta(hours=-5))
MIN_GAP = 3.0
BOARD_AGE = 900
_TIME_RE = re.compile(r"(\d+):(\d\d):(\d\d)")
_ENTRY_RE = re.compile(r'leaderboard-time">[^<]*?(\d+:\d\d:\d\d)')
_last = 0.0

def _config(key):
    if v := os.environ.get(key):
        return v
    env = ROOT / ".env"
    if env.exists():
        for line in env.read_text(encoding="utf-8-sig").splitlines():
            k, sep, v = line.partition("=")
            if sep and k.strip() == key:
                return v.strip().strip("\"'")
    raise RuntimeError(f"{key} is not set (environment variable or {env})")

def _get(path, auth=True):
    """GET BASE + path, at most one request per MIN_GAP seconds."""
    global _last
    if (wait := _last + MIN_GAP - time.monotonic()) > 0:
        time.sleep(wait)
    headers = {"User-Agent": _config("AOC_USER_AGENT")}
    if auth:
        headers["Cookie"] = f"session={_config('AOC_SESSION')}"
    try:
        with urlopen(Request(BASE + path, headers=headers), timeout=30) as r:
            return r.read().decode()
    except HTTPError as e:
        hint = {400: "session cookie invalid or expired", 500: "session cookie invalid or expired",
                404: "not found, or not unlocked yet"}.get(e.code, e.reason)
        raise RuntimeError(f"GET {path}: HTTP {e.code} ({hint})") from None
    finally:
        _last = time.monotonic()

def _cached(name, path, max_age, auth=True):
    """Body of path, reusing CACHE/name while younger than max_age seconds (None: forever)."""
    f = CACHE / name
    if f.exists() and (max_age is None or time.time() - f.stat().st_mtime < max_age):
        return f.read_text(encoding="utf-8")
    body = _get(path, auth)
    CACHE.mkdir(exist_ok=True)
    f.write_text(body, encoding="utf-8", newline="")
    return body

def _secs(tok):
    if m := _TIME_RE.fullmatch(tok):
        h, mi, s = map(int, m.groups())
        return h * 3600 + mi * 60 + s
    return inf if tok.startswith(">") else None

def days_in(year):
    """Number of puzzles in a year (AoC went to 12 days from 2025)."""
    return 12 if year >= 2025 else 25

def unlock_time(year, day):
    """When a puzzle unlocks: midnight US Eastern (UTC-5) on Dec <day>."""
    return datetime(year, 12, day, tzinfo=EST)

def unlocked(year, day):
    return datetime.now(EST) >= unlock_time(year, day)

def fetch_input(day=None, year=None, force=False):
    """Download your input to <year>/day_XX/day_XX.txt unless it is already there (non-empty); returns the path."""
    day, year = day or infer_day(), year or infer_year()
    f = input_path(day, year)
    if not force and f.exists() and f.stat().st_size:
        return f
    if not unlocked(year, day):
        raise RuntimeError(f"{year} day {day} unlocks at {unlock_time(year, day):%Y-%m-%d %H:%M} UTC-5")
    f.parent.mkdir(parents=True, exist_ok=True)
    f.write_text(_get(f"/{year}/day/{day}/input"), encoding="utf-8", newline="")
    return f

def answers_path(year):
    return ROOT / str(year) / "answers.json"

def fetch_answers(year, days=None, force=False):
    """Fill <year>/answers.json ({"01": [part1, part2], ...}) from the "Your puzzle answer was" lines on solved puzzle pages.

    Days already complete are not re-requested unless force; the last day only ever has one answer.
    """
    f = answers_path(year)
    ans = json.loads(f.read_text(encoding="utf-8-sig")) if f.exists() else {}
    for d in days or range(1, days_in(year) + 1):
        if not unlocked(year, d):
            break
        k, have = f"{d:02}", ans.get(f"{d:02}", [None, None])
        if not force and have[0] is not None and (have[1] is not None or d == days_in(year)):
            continue
        found = [unescape(a) for a in re.findall(r"Your puzzle answer was <code>(.*?)</code>", _get(f"/{year}/day/{d}"))]
        ans[k] = (found + [None, None])[:2]
        f.write_text(json.dumps(dict(sorted(ans.items())), indent=1), encoding="utf-8")
    return ans

def personal_stats(year, max_age=BOARD_AGE):
    """Your stats from /<year>/leaderboard/self: {day: {"time": [s1, s2], "rank": [r1, r2]}}.

    Times are seconds after unlock (inf when over 24h, None when unsolved); ranks are None where the page has none.
    """
    text = unescape(re.sub(r"<[^>]+>", "", _cached(f"self_{year}.html", f"/{year}/leaderboard/self", max_age)))
    out = {}
    for line in text.splitlines():
        toks = line.split()
        if not toks or not toks[0].isdigit() or not 1 <= int(toks[0]) <= 25:
            continue
        rest = toks[1:]
        # rows are "day time rank score time rank score", or just "day time time" on pages without ranks
        if len(rest) == 6:
            ts, rs = [rest[0], rest[3]], [rest[1], rest[4]]
        elif len(rest) == 2:
            ts, rs = rest, ["-", "-"]
        else:
            continue
        out[int(toks[0])] = {"time": list(map(_secs, ts)), "rank": [int(r) if r.isdigit() else None for r in rs]}
    return out

def global_cutoffs(year, days=None):
    """Seconds after unlock of the 100th solver of each part on the global leaderboard: {day: [s1, s2]}.

    The global leaderboard ended after 2024. Pages older than a day never change, so they are cached for good.
    """
    if year >= 2025:
        raise ValueError("AoC has no global leaderboard from 2025 on")
    out = {}
    for d in days or range(1, days_in(year) + 1):
        if not unlocked(year, d):
            break
        age = None if datetime.now(EST) > unlock_time(year, d) + timedelta(days=1) else BOARD_AGE
        html = _cached(f"global_{year}_{d:02}.html", f"/{year}/leaderboard/day/{d}", age, auth=False)
        # the page lists the both-stars top 100 first, then the first-star top 100
        both, _, first = html.partition("leaderboard-daydesc-first")
        out[d] = [_secs(t[-1]) if (t := _ENTRY_RE.findall(part)) else None for part in (first, both)]
    return out

def private_leaderboard(year, board_id):
    """A private leaderboard's JSON; the maintainer asks for at most one fetch per 15 minutes, so it is cached that long."""
    return json.loads(_cached(f"private_{year}_{board_id}.json",
                              f"/{year}/leaderboard/private/view/{board_id}.json", BOARD_AGE))

def star_times(board, member=None):
    """{day: [s1, s2]} seconds after unlock for one private leaderboard member (default: the board's owner)."""
    year = int(board["event"])
    days = board["members"][str(member or board["owner_id"])]["completion_day_level"]
    return {int(d): [int(p[k]["get_star_ts"] - unlock_time(year, int(d)).timestamp()) if k in p else None
                     for k in ("1", "2")] for d, p in sorted(days.items(), key=lambda kv: int(kv[0]))}

def _days(args, year):
    if not args:
        return range(1, days_in(year) + 1)
    out = []
    for a in args:
        lo, _, hi = a.partition("-")
        out += range(int(lo), int(hi or lo) + 1)
    return out

def main():
    if len(sys.argv) < 3:
        sys.exit(__doc__)
    cmd, year, *rest = sys.argv[1:]
    year = int(year)
    try:
        match cmd:
            case "input":
                for d in _days(rest, year):
                    had = (f := input_path(d, year)).exists() and f.stat().st_size
                    try:
                        fetch_input(d, year)
                        print(f"day {d:02}: {'cached' if had else 'fetched'}")
                    except RuntimeError as e:
                        print(f"day {d:02}: {e}")
            case "answers":
                for d, a in fetch_answers(year, _days(rest, year)).items():
                    print(f"day {d}: {a}")
            case "stats":
                for d, s in sorted(personal_stats(year).items()):
                    print(f"day {d:02}: {s}")
            case "cutoffs":
                for d, t in global_cutoffs(year).items():
                    print(f"day {d:02}: {t}")
            case _:
                sys.exit(__doc__)
    except RuntimeError as e:
        sys.exit(str(e))

if __name__ == "__main__":
    main()
