"""Completion-time plots.

CLI: python -m utils.plot <year> [part] [out.png]
  Compares your times with the global 100th place (before 2025), or with your private
  leaderboard's median when AOC_BOARD is set in .env / the environment.
"""
lazy import matplotlib.pyplot as plt
lazy from matplotlib.ticker import MaxNLocator
lazy from .api import _config, board_median, global_cutoffs, personal_stats, private_leaderboard
import sys
from math import isfinite, nan

def _series(times, part):
    """Split {day: [secs1, secs2]} into (days, minutes) for one part; unsolved/over-24h days become nan gaps."""
    days = sorted(times)
    return days, [t / 60 if (t := times[d][part - 1]) is not None and isfinite(t) else nan for d in days]

def _show(fig, out):
    """Save fig to out (a path) or show it."""
    if out:
        fig.savefig(out, dpi=150, bbox_inches="tight")
        plt.close(fig)
    else:
        plt.show()

def _finish(ax, title, out):
    """Apply shared styling, then save or show."""
    ax.set_title(title)
    ax.grid(alpha=0.3)
    ax.xaxis.set_major_locator(MaxNLocator(integer=True))
    if ax.get_legend_handles_labels()[0]:
        ax.legend()
    _show(ax.figure, out)

def plot_times(times, compare=None, part=2, title=None, out=None):
    """Plot your completion time per day against other series on a log scale.

    times: {day: [secs1, secs2]}. compare: {label: {day: [secs1, secs2]}}, e.g. a global cutoff or a
    leaderboard median. part: 1 or 2. out: save to this path instead of showing.
    """
    _, ax = plt.subplots(figsize=(10, 5))
    for label, series in {"You": times, **(compare or {})}.items():
        ax.plot(*_series(series, part), marker="o", label=label)
    ax.set_yscale("log")
    ax.set_xlabel("Day")
    ax.set_ylabel("Minutes after unlock")
    _finish(ax, title or f"Part {part} completion times", out)

def plot_years(years, part=2, out=None):
    """Plot your completion times for several years on one chart; years maps year -> {day: [secs1, secs2]}."""
    _, ax = plt.subplots(figsize=(10, 5))
    for y, times in sorted(years.items()):
        ax.plot(*_series(times, part), marker="o", label=str(y))
    ax.set_yscale("log")
    ax.set_xlabel("Day")
    ax.set_ylabel("Minutes after unlock")
    _finish(ax, f"Part {part} completion times by year", out)

def plot_ranks(ranks, title="Ranks", out=None):
    """Plot your rank per day for both parts; ranks maps day -> [rank1, rank2] (None if absent)."""
    _, ax = plt.subplots(figsize=(10, 5))
    days = sorted(ranks)
    for p in (1, 2):
        ax.plot(days, [nan if (r := ranks[d][p - 1]) is None else r for d in days], marker="o", label=f"Part {p}")
    ax.invert_yaxis()
    ax.set_xlabel("Day")
    ax.set_ylabel("Rank")
    _finish(ax, title, out)

def plot_grid(grid, cmap="viridis", title=None, out=None):
    """Show a Grid as an image; char grids get one colour per distinct character."""
    vals = list(grid.data)
    if grid.is_char:
        codes = {c: i for i, c in enumerate(sorted(set(vals)))}
        vals = [codes[v] for v in vals]
    fig, ax = plt.subplots()
    im = ax.imshow([vals[y * grid.w:(y + 1) * grid.w] for y in range(grid.h)], cmap=cmap, interpolation="nearest")
    if grid.is_char:
        cb = fig.colorbar(im, ticks=list(codes.values()))
        cb.ax.set_yticklabels([repr(chr(c)) for c in codes])
    ax.set_title(title or "")
    _show(fig, out)

def plot_points(points, path=None, title=None, out=None):
    """Scatter (x, y) points with y pointing down like AoC grids; path is an optional ordered list of points to draw."""
    fig, ax = plt.subplots()
    if points:
        ax.scatter(*zip(*points), s=4)
    if path:
        ax.plot(*zip(*path), color="red", linewidth=1)
    ax.invert_yaxis()
    ax.set_aspect("equal")
    ax.set_title(title or "")
    _show(fig, out)

def main():
    if not 2 <= len(sys.argv) <= 4:
        sys.exit(__doc__)
    year, part, out = int(sys.argv[1]), int(sys.argv[2]) if len(sys.argv) > 2 else 2, sys.argv[3] if len(sys.argv) > 3 else None
    try:
        mine = {d: s["time"] for d, s in personal_stats(year).items()}
        compare = {}
        if year < 2025:
            compare["Global 100th"] = global_cutoffs(year)
        if board := _config("AOC_BOARD", False):
            compare["Board median"] = board_median(private_leaderboard(year, board))
    except RuntimeError as e:
        sys.exit(str(e))
    plot_times(mine, compare, part, f"{year} part {part} completion times", out)

if __name__ == "__main__":
    main()
