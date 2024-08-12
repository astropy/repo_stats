import os
import time
from datetime import datetime, timezone
import subprocess
import requests
import numpy as np
import ast

from repo_stats.utilities import fill_missed_months, update_cache


class GitMetrics:
    def __init__(self, token, repo_owner, repo_name, cache_dir):
        """
        Class for getting and processing repository data (commit history, issues, pull requests, contributors) from GitHub for a given repository.

        Arguments
        ---------
        token : str
            Authorization token for GitHub queries
        repo_owner : str
            Owner (or organization) of repository on GitHub
        repo_name : str
            Name of repository on GitHub
        cache_dir : str, default=None
            Path to directory that will be populated with caches of git data
        """
        self.token = token
        self.repo_owner = repo_owner
        self.repo_name = repo_name
        self.cache_dir = cache_dir

