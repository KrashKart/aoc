lazy import matplotlib.pyplot as plt
from math import isfinite


def _series(times, part):
    """Split {day: [secs1, secs2]} into (days, minutes) for one part, skipping unsolved/over-24h entries."""
    pts = [(d, t[part - 1] / 60) for d, t in sorted(times.items()) if t[part - 1] is not None and isfinite(t[part - 1])]
    return [d for d, _ in pts], [m for _, m in pts]


def _finish(ax, title, out):
    """Apply shared styling, then save to out (a path) or show the figure."""
    ax.set_title(title)
    ax.grid(alpha=0.3)
    ax.legend()
    if out:
        ax.figure.savefig(out, dpi=150, bbox_inches="tight")
        plt.close(ax.figure)
    else:
        plt.show()


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
    for p in (1, 2):
        pts = [(d, r[p - 1]) for d, r in sorted(ranks.items()) if r[p - 1] is not None]
        ax.plot([d for d, _ in pts], [r for _, r in pts], marker="o", label=f"Part {p}")
    ax.invert_yaxis()
    ax.set_xlabel("Day")
    ax.set_ylabel("Rank")
    _finish(ax, title, out)


def plot_grid(grid, cmap="viridis", title=None):
    """Show a Grid as an image; char grids get one colour per distinct character."""
    vals = list(grid.data)
    if grid.is_char:
        codes = {c: i for i, c in enumerate(sorted(set(vals)))}
        vals = [codes[v] for v in vals]
    _, ax = plt.subplots()
    im = ax.imshow([vals[y * grid.w:(y + 1) * grid.w] for y in range(grid.h)], cmap=cmap, interpolation="nearest")
    if grid.is_char:
        cb = plt.colorbar(im, ticks=list(codes.values()))
        cb.ax.set_yticklabels([repr(chr(c)) for c in codes])
    ax.set_title(title or "")
    plt.show()


def plot_points(points, path=None, title=None):
    """Scatter (x, y) points with y pointing down like AoC grids; path is an optional ordered list of points to draw."""
    _, ax = plt.subplots()
    if points:
        ax.scatter(*zip(*points), s=4)
    if path:
        ax.plot(*zip(*path), color="red", linewidth=1)
    ax.invert_yaxis()
    ax.set_aspect("equal")
    ax.set_title(title or "")
    plt.show()
