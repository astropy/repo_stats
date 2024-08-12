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

    def get_citations(self, bib, metric):
        """
        Get citation data for a paper with the identifier 'bib' by quering the ADS API.

        Arguments
        ---------
        bib : str
            Bibcode identifier of the paper being cited, e.g., "2013A&A...558A..33A"
        metric : str
            Metrics to return for each citation to the paper, e.g. "bibcode, pubdate, pub, author, title"

        Returns
        -------
        all_cites : list of dict
            For each citation to the paper 'bib', a dictionary of 'metric' data
        """
        cache_file = f"{self.cache_dir}/{bib}.txt"
        if not os.path.exists(cache_file):
            open(cache_file, "w").close()

        with open(cache_file, "r") as f:
            old_cites = f.readlines()
            print(f"  {len(old_cites)} citations found in ADS cache at {cache_file}")

        if old_cites is None:
            end, start = 1, 0
        else:
            end, start = len(old_cites) + 1, len(old_cites)

        new_cites = []
        while end > start:
            encoded_query = urlencode(
                {
                    "q": f"citations({bib})",
                    "fl": metric,
                    "rows": 100,
                    "start": start,
                }
            )

            response = requests.get(
                f"https://api.adsabs.harvard.edu/v1/search/query?{encoded_query}",
                headers={
                    "Authorization": "Bearer " + self.token,
                    "Content-type": "application/json",
                },
            )
            if response.status_code == 200:
                result = response.json()["response"]

                new_cites.extend(result["docs"])
                end, start = result["numFound"], result["start"] + len(result["docs"])

            else:
                raise Exception(f"Query failed -- return code {response.status_code}")

        all_cites = update_cache(cache_file, old_cites, new_cites)

        return all_cites

