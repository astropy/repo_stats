from datetime import datetime, timezone

import matplotlib.pyplot as plt
from matplotlib.lines import Line2D

from repo_stats.utilities import rolling_average

ms = [".", "+", "^", "*", "x", "o"]
cs = ["#ff8300", "#23d361", "#bf177a", "#20c8ed"]

plt.rcParams['font.size'] = 11

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

    plt.xticks(ticks=months[::12], labels=[x[:4] for x in months[::12]])#, rotation=90)

    plt.title(
        f"Unique authors of commits to {repo_owner}/{repo_name} (generated on {now})"
    )
    plt.legend()
    plt.xlabel(f"Date ({datetime.strptime(months[0], '%Y-%m').strftime('%B')} of each year)")
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


def open_issue_PR_plot(issue_pr_stats, repo_name, cache_dir):
    """
    Plot a bar chart of a repository's currently open issues and pull requests.

    Arguments
    ---------
    issue_pr_stats : list of dict
        Statistics for issues and pull requests (see `git_metrics.Gits.process_issues_PRs`)
    repo_name : str
        Name of repository (for labels and figure savename)
    cache_dir : str
        Name of directory in which to cache figure

    Returns
    -------
    fig : `plt.figure` instance
        The generated figure
    """
    print("\nMaking figure: currently open issues and pull requests")

    labels = issue_pr_stats["issues"]["label_open"].keys()
    open_issues = issue_pr_stats["issues"]["label_open"].values()
    open_prs = issue_pr_stats["pullRequests"]["label_open"].values()

    fig = plt.figure(figsize=(10, 6))

    plt.bar(labels, open_issues, color=cs[3], label="Open issues")
    plt.bar(labels, open_prs, color="r", alpha=0.4, label="Open PRs")

    plt.xticks(rotation=90)

    plt.title(f"Open issues and PRs per {repo_name} subpackage (generated on {now})")
    plt.legend()
    plt.xlabel("Subpackage")
    plt.ylabel("N")
    plt.tight_layout()
    plt.savefig(f"{cache_dir}/{repo_name}_open_items.png", dpi=300)
    # plt.show(block=False)

    return fig


def issue_PR_time_plot(issue_pr_stats, repo_owner, repo_name, cache_dir, window_avg=7):
    """
    Plot a repository's number of issues and pull requests open and closed over time.

    Arguments
    ---------
    issue_pr_stats : list of dict
        Statistics for issues and pull requests (see `git_metrics.Gits.process_issues_PRs`)
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
    print("\nMaking figure: issues and pull requests over time")

    month_io, issue_open = issue_pr_stats["issues"]["open_per_month"]
    month_ic, issue_close = issue_pr_stats["issues"]["close_per_month"]
    month_po, pr_open = issue_pr_stats["pullRequests"]["open_per_month"]
    month_pc, pr_close = issue_pr_stats["pullRequests"]["close_per_month"]

    # don't include current month (if it's early in the month, result biased low)
    months = [
        month_po[:-1],
        month_pc[:-1],
        month_io[:-1],
        month_ic[:-1],
    ]
    events = [
        pr_open[:-1],
        pr_close[:-1],
        issue_open[:-1],
        issue_close[:-1],
    ]
    labels = [
        "PRs opened / month",
        "PRs closed / month",
        "Issues opened / month",
        "Issues closed / month",
    ]

    fig = plt.figure(figsize=(10, 6))
    for i, j in enumerate(events):
        plt.plot(months[i], j, cs[i], alpha=0.2, label=labels[i])

        roll_avg, window_avg = rolling_average(j, window_avg)
        cut_idx = window_avg // 2
        plt.plot(
            months[i][cut_idx:-cut_idx],
            roll_avg,
            cs[i],
            label=f"{labels[i]}: {window_avg} month rolling average",
        )

    plt.xticks(ticks=months[i][::12], labels=[x[:4] for x in months[i][::12]])#, rotation=90)

    plt.title(
        f"Issues and PRs opened and closed in {repo_owner}/{repo_name} (generated on {now})"
    )
    plt.legend(ncol=2)
    plt.xlabel(f"Date ({datetime.strptime(months[i][0], '%Y-%m').strftime('%B')} of each year)")
    plt.ylabel("N")
    plt.tight_layout()
    plt.savefig(f"{cache_dir}/{repo_name}_issues_PRs.png", dpi=300)
    # plt.show(block=False)

    return fig
