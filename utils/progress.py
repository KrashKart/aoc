"""README progress: badges/<year>.svg star bars and badges/times_<year>.png part 1 and 2 completion-time charts.

Times come from the private leaderboard AOC_BOARD (exact, as member AOC_USER_ID or the board's owner) when
set, else from your self page, where anything over 24h has no time and shows as a gap.

CLI: python -m utils.progress
"""
lazy from .plot import plot_parts
from .api import _config, days_in, personal_stats, private_leaderboard, star_times, unlocked
from .core import ROOT
import re

GOLD, SILVER, OPEN, LOCKED, BG, FG = "#f5c518", "#c0c0c0", "#3a3a52", "#23233a", "#0f0f23", "#e6e6e6"
BADGES = ROOT / "badges"

def all_years():
    """Every <year> folder whose first puzzle has unlocked."""
    return sorted(y for p in ROOT.iterdir() if p.is_dir() and p.name.isdigit() and unlocked(y := int(p.name), 1))

def times(year):
    """{day: [s1, s2]} seconds after unlock, from the private board if configured, else the self page."""
    mine = {d: s["time"] for d, s in personal_stats(year).items()}
    if not (board := _config("AOC_BOARD", False)):
        return mine
    if not (exact := star_times(private_leaderboard(year, board), member := _config("AOC_USER_ID", False))) and mine:
        raise RuntimeError(f"board {board} has no {year} stars for {'member ' + member if member else 'its owner'}: "
                           "set AOC_USER_ID in .env to your id (adventofcode.com/settings)")
    return exact

def stars(year):
    """(gold days, silver days, unlocked stars, total stars) for a year; silver means part 1 only."""
    got = [sum(t is not None for t in s["time"]) for s in personal_stats(year).values()]
    n = days_in(year)
    return got.count(2), got.count(1), 2 * sum(unlocked(year, d) for d in range(1, n + 1)), 2 * n

def badge_svg(year, gold, silver, avail, total, w=360, h=28):
    """An SVG bar: gold and silver star segments, then unlocked-but-unsolved, then still-locked stars."""
    x0, bw, bh = 52, w - 52 - 110, 10
    u = bw / total
    segs, x = [], x0
    for n, c in ((2 * gold, GOLD), (silver, SILVER), (avail - 2 * gold - silver, OPEN), (total - avail, LOCKED)):
        if n > 0:
            segs.append(f'<rect x="{x:.1f}" y="{(h - bh) / 2}" width="{n * u:.1f}" height="{bh}" fill="{c}"/>')
            x += n * u
    font = 'font-family="Consolas,Menlo,monospace" font-size="13"'
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">'
            f'<title>{year}: {2 * gold + silver}/{total} stars ({gold} gold, {silver} silver)</title>'
            f'<rect width="{w}" height="{h}" rx="5" fill="{BG}"/>'
            f'<text x="10" y="{h / 2 + 4.5}" fill="{FG}" {font}>{year}</text>'
            f'<clipPath id="c"><rect x="{x0}" y="0" width="{bw}" height="{h}" rx="3"/></clipPath>'
            f'<g clip-path="url(#c)">{"".join(segs)}</g>'
            f'<text x="{x0 + bw + 10}" y="{h / 2 + 4.5}" {font}><tspan fill="{GOLD}">{2 * gold + silver}</tspan>'
            f'<tspan fill="{FG}">/{total} ★</tspan><tspan fill="{SILVER}">{f" ({silver}☆)" if silver else ""}</tspan></text>'
            '</svg>')

def _set_block(text, name, body, heading):
    """Replace the <!-- name --> block in text, or append it under a new # heading."""
    block = f"<!-- {name} -->\n{body}\n<!-- /{name} -->"
    mark = re.compile(rf"<!-- {name} -->.*?<!-- /{name} -->", re.S)
    return mark.sub(lambda _: block, text) if mark.search(text) else f"{text.rstrip()}\n\n# {heading}\n{block}\n"

def update_readme(years=None):
    """Write each year's badge and times chart, then refresh the README progress and times blocks (newest year first)."""
    years = sorted(years or all_years(), reverse=True)
    BADGES.mkdir(exist_ok=True)
    src = "private leaderboard" if _config("AOC_BOARD", False) else "self page, >24h shown as gaps"
    badges, charts = [], []
    for y in years:
        (BADGES / f"{y}.svg").write_text(badge_svg(y, *(s := stars(y))), encoding="utf-8")
        badges.append(f"![{y}: {2 * s[0] + s[1]}/{s[3]} stars](badges/{y}.svg)  ")
        print(f"  {y}: {s[0]} gold, {s[1]} silver, {2 * s[0] + s[1]}/{s[2]} unlocked, {s[3]} total", flush=True)
        plot_parts(times(y), f"{y} completion times", BADGES / f"times_{y}.png")
        charts.append(f"![{y} Part 1 and 2 completion times](badges/times_{y}.png)")
        print(f"  chart: badges/times_{y}.png ({src})", flush=True)
    readme = ROOT / "README.md"
    text = _set_block(readme.read_text(encoding="utf-8"), "progress", "\n".join(badges), "Progress by Year")
    readme.write_text(_set_block(text, "times", "\n".join(charts), "Completion Times by Year"), encoding="utf-8")

def main():
    try:
        update_readme()
    except RuntimeError as e:
        raise SystemExit(str(e))

if __name__ == "__main__":
    main()
