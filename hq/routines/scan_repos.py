import git
import datetime
from dateutil import tz


repo_list = [
    ('/home/sarai/github-projects/follow-up-projects/knowledge', 'https://github.com/nikitavoloboev/knowledge'),
    ('/home/sarai/github-projects/second-brain', 'https://github.com/rsarai/second-brain'),
]


def get_compare_link_for(repo, repo_url, min_date, max_date):
    commits = [
        commit
        for commit in repo.iter_commits(rev=repo.head.reference)
        if commit.authored_datetime < max_date and commit.authored_datetime > min_date
    ]

    commit1 = commits[-1]
    commit2 = commits[0]
    return f"{repo_url}/compare/{commit1}..{commit2}"


def get_last_week_dates():
    now = datetime.datetime.now(tz.tzlocal())
    today = now.replace(hour=0, minute=0, second=0, microsecond=0)
    start_date = today + datetime.timedelta(-today.weekday() - 1, weeks=-1)
    end_date = today + datetime.timedelta(-today.weekday() - 2)
    end_date = end_date.replace(hour=23, minute=59, second=59, microsecond=0)
    return start_date, end_date


def get_yesterday_dates():
    now = datetime.datetime.now(tz.tzlocal())
    today = now.replace(hour=0, minute=0, second=0, microsecond=0)
    yesterday = today - datetime.timedelta(days=1)
    max_date = yesterday.replace(hour=23, minute=59, second=59, microsecond=0)
    min_date = yesterday = today - datetime.timedelta(days=1)
    return min_date, max_date


def scan():
    min_date, max_date = get_last_week_dates()
    print(min_date, max_date)

    for repo_path, repo_url in repo_list:
        repo = git.Repo(repo_path)
        repo.remotes.origin.pull()

        print(get_compare_link_for(repo, repo_url, min_date=min_date, max_date=max_date))
