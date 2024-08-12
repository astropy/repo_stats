import os
from datetime import datetime, timedelta, timezone
from urllib.parse import urlencode

import numpy as np
import requests

from repo_stats.utilities import update_cache


class ADSCitations:
    def __init__(self, token, cache_dir):
        """
        Class for getting, processing and aggregating citation data from the NASA ADS database for a given set of papers.

        Arguments
        ---------
        token : str
            Authorization token for ADS queries
        cache_dir : str, default=None
            Path to directory that will be populated with caches of citation data
        """
        self.token = token
        self.cache_dir = cache_dir
