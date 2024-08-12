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

    def get_age(self, date):
        """
        Get the 'datetime' age of a string 'date'

        Arguments
        ---------
        date : str
            Dates with assumed string format "2024-01-01..."

        Returns
        -------
        age : 'datetime.timedelta' instance or int
            Age of the item (int if 'days_since' is True)

        """
        if date is None:
            return -1

        now = datetime.now(timezone.utc)
        date_utc = datetime.strptime(date[:10], "%Y-%m-%d").replace(tzinfo=timezone.utc)
        age = now - date_utc

        return age

    def parse_log_line(self, line):
        """
        Break an individual 'git log' line 'line' into its component parts (commit hash, date, author).

        Arguments
        ---------
        line : str
            Dates with assumed string format "2024-01-01..."

        Returns
        -------
        parsed : list of str
            The commit's hash, date, author
        """
        line = line.split(",")
        parsed = []
        for ii in range(3):
            parsed.append(line[ii].lstrip('"').rstrip('"\n'))

        return parsed

    def get_commits(self):
        """
        Obtain the commit history for a repository with 'git log', and parse the output.

        Returns
        -------
        all_items : list of dict
            A dictionary entry for each commit in the history, including the identifiers below in 'query'
        """
        print("\nCollecting git commit history")

        cache_file = f"{self.cache_dir}/{self.repo_name}_commits.txt"
        if not os.path.exists(cache_file):
            open(cache_file, "w").close()

        with open(cache_file, "r") as f:
            old_items = f.readlines()
            print(f"  {len(old_items)} commits found in cache at {cache_file}")
        if old_items == []:
            # NOTE: 'after' here differs from GitMetrics.get_issues_PRs, as does its type in 'query' below ('String' vs. 'String!') - see https://github.com/orgs/community/discussions/24443
            after = None
        else:
            # convert string to dict and get relevant key
            after = ast.literal_eval(old_items[-1].rstrip("\n"))["endCursor"]

        # For query syntax, see https://docs.github.com/en/graphql/reference/objects#repository
        # and https://docs.github.com/en/graphql/reference/objects#commit
        # and https://docs.github.com/en/graphql/reference/objects#gitactor
        # and https://docs.github.com/en/graphql/guides/using-pagination-in-the-graphql-api
        # To quickly test a query, try https://docs.github.com/en/graphql/overview/explorer
        query = """
        query($owner: String!, $name: String!, $after: String) {
            repository(name: $name, owner: $owner) {
                ref(qualifiedName: "main") {
                    target {
                        ... on Commit {                    
                            history(first: 100, after: $after) {
                                pageInfo {
                                    hasNextPage
                                    endCursor
                                }
                        
                                edges {
                                    node {
                                        oid
                                        authoredDate
                                        author {
                                            name
                                            email
                                            user {
                                                databaseId
                                            }
                                        }
                                    }
                                }
                            }
                        }
                    }
                }
            }
        }                
        """

        headers = {"Authorization": f"token {self.token}"}
        # with 'after', traverse through items (issues or PRs) from oldest to newest
        variables = {
            "owner": self.repo_owner,
            "name": self.repo_name,
            "after": after,
        }
        # must traverse through pages of items
        hasNextPage = True

        new_items = []
        items_retrieved = 0
        while hasNextPage is True:
            response = requests.post(
                "https://api.github.com/graphql",
                json={"query": query, "variables": variables},
                headers=headers,
            )

            if response.status_code == 200:
                result = response.json()
                try:
                    result["data"]
                except KeyError as err:
                    print(f"Query syntax is likely wrong. Reponse to query: {result}")
                    raise err

                items_retrieved += len(
                    result["data"]["repository"]["ref"]["target"]["history"]["edges"]
                )

                time_to_reset = datetime.fromtimestamp(
                    int(response.headers["X-RateLimit-Reset"]) - time.time(),
                    tz=timezone.utc,
                ).strftime("%M:%S")

                if (
                    len(
                        result["data"]["repository"]["ref"]["target"]["history"][
                            "edges"
                        ]
                    )
                    > 0
                ):
                    print(
                        f"\r  Retrieved {items_retrieved} new commits (rate limit used: {response.headers['X-RateLimit-Used']} of {response.headers['X-RateLimit-Limit']} - resets in {time_to_reset})",
                        end="",
                        flush=True,
                    )

                    # store ID of the chronologically newest commit on current page, used to later reference newest item in cache
                    result["data"]["repository"]["ref"]["target"]["history"]["edges"][
                        -1
                    ]["endCursor"] = result["data"]["repository"]["ref"]["target"][
                        "history"
                    ][
                        "pageInfo"
                    ][
                        "endCursor"
                    ]
                    new_items.extend(
                        result["data"]["repository"]["ref"]["target"]["history"][
                            "edges"
                        ]
                    )

                hasNextPage = result["data"]["repository"]["ref"]["target"]["history"][
                    "pageInfo"
                ]["hasNextPage"]

                variables["after"] = result["data"]["repository"]["ref"]["target"][
                    "history"
                ]["pageInfo"]["endCursor"]

            else:
                raise Exception(f"Query failed -- return code {response.status_code}")

        # prevent last flush, without printing new line
        print("", end="")

        all_items = update_cache(cache_file, old_items, new_items)

        return all_items

