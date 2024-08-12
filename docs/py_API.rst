repo_stats API
==============

citation_metrics
----------------

.. currentmodule:: repo_stats.citation_metrics

.. autoclass:: repo_stats.citation_metrics.ADSCitations
  :members: get_citations, process_citations, aggregate_citations

git_metrics
-----------

.. currentmodule:: repo_stats.git_metrics

.. autoclass:: repo_stats.git_metrics.GitMetrics
  :members: get_age, parse_log_line, get_commits, get_commits_via_git_log, process_commits, get_issues_PRs, process_issues_PRs

plot
----

.. currentmodule:: repo_stats.plot

.. autofunction:: author_time_plot

.. autofunction:: citation_plot

.. autofunction:: open_issue_PR_plot

.. autofunction:: issue_PR_time_plot

runner
------

.. currentmodule:: repo_stats.runner

.. autofunction:: parse_parameters

.. autofunction:: main

user_stats
----------

.. currentmodule:: repo_stats.user_stats

.. autoclass:: repo_stats.user_stats.StatsImage
  :members: draw_text, update_image

utilities
---------

.. currentmodule:: repo_stats.utilities

.. autofunction:: fill_missed_months

.. autofunction:: rolling_average

.. autofunction:: update_cache
