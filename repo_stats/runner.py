import argparse
import json
import os
from pathlib import Path

import repo_stats

# from dotenv import load_dotenv
from repo_stats.citation_metrics import ADSCitations
from repo_stats.git_metrics import GitMetrics
from repo_stats.plot import (
    author_time_plot,
    citation_plot,
    issue_PR_time_plot,
    open_issue_PR_plot,
)
from repo_stats.user_stats import StatsImage

repo_stats_path = os.path.dirname(repo_stats.__file__)


def parse_parameters(*args):
    """
    Read the repository and citation targets and the analysis parameters from a .json parameter file.

    Parameters
    ----------
    *args : list of str
        Simulates the command line arguments

    Returns
    -------
    params : dict
        Parameters used by the analysis
    """

    default_param_file = f"{repo_stats_path}/parameters.json"

    parser = argparse.ArgumentParser()

    parser.add_argument(
        "-a",
        "--ads_token",
        type=str,
        required=True,
    )

    parser.add_argument(
        "-g",
        "--git_token",
        type=str,
        required=True,
    )

    parser.add_argument(
        "-p",
        "--parameter_file",
        type=str,
        default=default_param_file,
        required=False,
    )

    parser.add_argument(
        "-c",
        "--cache_dir",
        type=str,
        required=False,
    )

    args = parser.parse_args(*args)

    params = json.load(open(args.parameter_file, "r"))
    params["ads_token"], params["git_token"], params["cache_dir"] = (
        args.ads_token,
        args.git_token,
        args.cache_dir,
    )

    if params["cache_dir"] is None:
        params["cache_dir"] = f"{repo_stats_path}/../cache"
    Path(params["cache_dir"]).mkdir(parents=True, exist_ok=True)

    if params["template_image"] is None:
        params["template_image"] = [
            f"{repo_stats_path}/../dashboard_template/user_stats_template_dark.png",
            f"{repo_stats_path}/../dashboard_template/user_stats_template_light.png",
        ]
    params["template_image"] = list(params["template_image"])
    params["font"] = f"{repo_stats_path}/../dashboard_template/Jost[wght].ttf"

    return params


def main(*args):
    """
    Run the citation and repository statistics analysis.

    Parameters
    ----------
    *args : list of str
        Simulates the command line arguments
    """
    # load_dotenv()
    # params['ads_token'] = os.getenv('ADS_TOKEN')
    # params['git_token'] = os.getenv('GIT_TOKEN')
    params = parse_parameters(*args)

    Cites = ADSCitations(params["ads_token"], params["cache_dir"])
    cite_stats = Cites.aggregate_citations(params["bibs"], params["ads_metrics"])

    Gits = GitMetrics(
        params["git_token"],
        params["repo_owner"],
        params["repo_name"],
        params["cache_dir"],
    )

    commits = Gits.get_commits()
    commit_stats = Gits.process_commits(commits, params["age_recent_commit"])

    issues = Gits.get_issues_PRs("issues")
    prs = Gits.get_issues_PRs("pullRequests")
    issue_pr_stats = Gits.process_issues_PRs(
        [issues, prs],
        ["issues", "pullRequests"],
        params["labels"],
        params["age_recent_issue_pr"],
    )

    all_stats = {**cite_stats, **commit_stats, **issue_pr_stats}

    print("\nUpdating dashboard image with stats")
    background_colors = ["dark", "light"]
    for ii, jj in enumerate(params["template_image"]):
        UserStatsImage = StatsImage(jj, params["font"], color=background_colors[ii])
        UserStatsImage.update_image(all_stats, params["repo_name"], params["cache_dir"])

    citation_plot(
        cite_stats, params["repo_name"], params["cache_dir"], params["bib_names"]
    )

    author_time_plot(
        commit_stats,
        params["repo_owner"],
        params["repo_name"],
        params["cache_dir"],
        params["window_avg"],
    )

    open_issue_PR_plot(issue_pr_stats, params["repo_name"], params["cache_dir"])

    issue_PR_time_plot(
        issue_pr_stats,
        params["repo_owner"],
        params["repo_name"],
        params["cache_dir"],
        params["window_avg"],
    )


if __name__ == "__main__":
    main()
