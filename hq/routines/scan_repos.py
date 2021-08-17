import git
import datetime
from dateutil import tz


# now = datetime.datetime.now(tz.tzlocal())
# today = now.replace(hour=0, minute=0, second=0, microsecond=0)
# yesterday = today - datetime.timedelta(days=1)
# last_first_weekday = today - datetime.timedelta(days=now.weekday())
# last_first_monthday = today.replace(day=1)
# last_first_yearday = today.replace(day=1, month=1)

repo = git.Repo('/home/sarai/github-projects/follow-up-projects/knowledge')
repo.remotes.origin.pull()


def get_compare_link_for(min_date, max_date):
    commits = [
        commit
        for commit in repo.iter_commits(rev=repo.head.reference)
        if commit.authored_datetime < max_date and commit.authored_datetime > min_date
    ]

    commit1 = commits[-1]
    commit2 = commits[0]
    return f"https://github.com/nikitavoloboev/knowledge/compare/{commit1}..{commit2}"


def scan():
    now = datetime.datetime.now(tz.tzlocal())
    today = now.replace(hour=0, minute=0, second=0, microsecond=0)
    yesterday = today - datetime.timedelta(days=1)
    max_date = yesterday.replace(hour=23, minute=59, second=59, microsecond=0)
    min_date = yesterday = today - datetime.timedelta(days=1)

    # Yesteday link
    print(get_compare_link_for(min_date=min_date, max_date=max_date))
