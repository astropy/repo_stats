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


def citation_plot(cite_stats, repo_name, cache_dir, names=None):
    """
    Plot citations to referenced papers over time.

    Arguments
    ---------
    cite_stats : dict
        Dictionary including citation statistics. See `citation_metrics.Cites.aggregate_citations()`
    repo_name : str
        Name of repository (for labels and figure savename)
    cache_dir : str
        Name of directory in which to cache figure
    names : list of str, optional
        Name of referenced papers (for plot legend)

    Returns
    -------
    fig : `plt.figure` instance
        The generated figure
    """
    print("\nMaking figure: citations over time")

    days_passed = datetime.today().month * 30.437 + datetime.today().day

    fig = plt.figure(figsize=(10, 6))
    for ii, xx in enumerate(cite_stats):
        cites = cite_stats[xx]["cite_per_year"]

        # remove one citation that has wrong year in ADS database
        if names[ii] == "Astropy paper II (2018)":
            cites[0], cites[1] = cites[0][1:], cites[1][1:]

        (line,) = plt.plot(
            cites[0][:-1],
            cites[1][:-1],
            marker=ms[ii],
            c=cs[ii],
        )
        if names is not None:
            line.set_label(f"{names[ii]}, N = {sum(cites[1])}")
        if names[ii] == "All unique citations":
            line.set_linestyle("--")

        plt.plot(
            cites[0][-1],
            cites[1][-1],
            marker=ms[-2],
            c=cs[ii],
        )
        plt.plot(
            cites[0][-1],
            int(cites[1][-1] * 365 / days_passed),
            marker=ms[-1],
            mec=cs[ii],
            mfc="none",
        )

    handles, _ = plt.gca().get_legend_handles_labels()
    point0 = Line2D(
        [0], [0], linestyle="", marker=ms[-2], label="Year-to-date", color="#a4a4a4"
    )
    point1 = Line2D(
        [0],
        [0],
        linestyle="",
        marker=ms[-1],
        label="Projected (using year-to-date)",
        markeredgecolor="#a4a4a4",
        markerfacecolor="none",
    )
    handles.extend([point0, point1])
    plt.legend(handles=handles)

    plt.title(f"Refereed citations to {repo_name} (via ADS) (generated on {now})")
    plt.xlabel("Year")
    plt.ylabel("N")
    plt.tight_layout()
    plt.savefig(f"{cache_dir}/{repo_name}_citations.png", dpi=300)
    # plt.show(block=False)

    return fig


