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
        params["cache_dir"] = f"{repo_stats_path}/../cache/{params['repo_name']}"
    Path(params["cache_dir"]).mkdir(parents=True, exist_ok=True)

    if params["template_image"] is None:
        params["template_image"] = [
            f"{repo_stats_path}/../dashboard_template/user_stats_template_dark.png",
            f"{repo_stats_path}/../dashboard_template/user_stats_template_light.png",
        ]
    params["template_image"] = list(params["template_image"])
    params["font"] = f"{repo_stats_path}/../dashboard_template/Jost[wght].ttf"

    return params

