from datetime import datetime, timezone

import matplotlib.pyplot as plt
from matplotlib.lines import Line2D

from repo_stats.utilities import rolling_average

ms = [".", "+", "^", "*", "x", "o"]
cs = ["#ff8300", "#23d361", "#bf177a", "#20c8ed"]

now = datetime.now(timezone.utc).strftime("%B %d, %Y")


def author_time_plot(commit_stats, repo_owner, repo_name, cache_dir, window_avg=7):
    """
    Plot respository commit authors over time.

    Arguments
    ---------
    commit_stats : dict
        Dictionary including commit statistics. See `git_metrics.Gits.process_commits()`
    repo_owner : str
        Owner of repository (for labels)
    repo_name : str
        Name of repository (for labels and figure savename)
    cache_dir : str
        Name of directory in which to cache figure
    window_avg : int, default=7
        Number of months for rolling average of commit data. Enforced to be odd.

    Returns
    -------
    fig : `plt.figure` instance
        The generated figure
    """
    print("\nMaking figure: commit authors over time")

    months, authors = commit_stats["authors_per_month"]
    months_multi_authors, multi_authors = commit_stats["multi_authors_per_month"]
    months_new_authors, new_authors = commit_stats["new_authors_per_month"]

    # don't include current month (if it's early in the month, result biased low)
    months = months[:-1]
    authors = authors[:-1]
    months_multi_authors = months_multi_authors[:-1]
    multi_authors = multi_authors[:-1]
    months_new_authors = months_new_authors[:-1]
    new_authors = new_authors[:-1]

    roll_avg, window_avg = rolling_average(authors, window_avg)
    roll_avg_multi, window_avg = rolling_average(multi_authors, window_avg)
    cut_idx = window_avg // 2

    fig = plt.figure(figsize=(10, 6))
    plt.plot(months, authors, "k", alpha=0.2, label="Authors / month")

    plt.plot(
        months[cut_idx:-cut_idx],
        roll_avg,
        "k",
        label=f"Authors / month: {window_avg} month rolling average",
    )

    plt.plot(
        months_multi_authors,
        multi_authors,
        "r",
        alpha=0.2,
        label="Authors with >1 commit / month",
    )
    plt.plot(
        months[cut_idx:-cut_idx],
        roll_avg_multi,
        "r",
        label=f"Authors with >1 commit / month: {window_avg} month rolling average",
    )

    plt.plot(months_new_authors, new_authors, cs[3], label="New authors / month")

    plt.axhline(0, c="k", ls="--")

    plt.xticks(months[::12], rotation=90)

    plt.title(
        f"Unique authors of commits to {repo_owner}/{repo_name} (generated on {now})"
    )
    plt.legend()
    plt.xlabel("Date")
    plt.ylabel("N")
    plt.tight_layout()
    plt.savefig(f"{cache_dir}/{repo_name}_authors.png", dpi=300)
    # plt.show(block=False)

    return fig


