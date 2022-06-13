import json
from typing import Optional
import pytz

from datetime import datetime
from pydantic import BaseModel

from hq.common import get_files, parse_datetime
from hq.config import Github as config


def get_events_file_paths():
    return get_files(config.export_path + "/events/", "*.json")


def get_notification_file_paths():
    return get_files(config.export_path + "/notifications/", "*[!_details].json")


def get_notification_detail_file_paths():
    return get_files(config.export_path + "/notifications/", "*_details.json")


class Notification(BaseModel):
    raw: dict
    github_id: Optional[int]
    reason: Optional[str]
    repository: Optional[dict]
    url: Optional[str]
    updated_at_str: Optional[str]
    updated_at: Optional[datetime]
    subject: Optional[dict]
    summary: Optional[str]

    def __init__(self, raw, details) -> None:
        data = {"raw": raw}
        data["github_id"] = raw["id"]
        data["reason"] = raw["reason"]
        data["repository"] = {
            "id": raw.get("repository", {}).get("id"),
            "name": raw.get("repository", {}).get("name"),
            "full_name": raw.get("repository", {}).get("full_name"),
            "private": raw.get("repository", {}).get("private"),
            "description": raw.get("repository", {}).get("description"),
            "url": raw.get("repository", {}).get("html_url"),
        }
        data["url"] = raw["url"]
        data["updated_at_str"] = raw["updated_at"]
        data["updated_at"] = parse_datetime(data["updated_at_str"], '%Y-%m-%dT%H:%M:%S%z')

        if details:
            key = data["github_id"] + data["updated_at_str"]

            if details.get(key):
                original = raw["subject"].copy()
                original.update(details[key])
                data["subject"] = original
            else:
                data["subject"] = raw["subject"]
        elif type(raw["subject"]):
            data["subject"] = raw["subject"]["title"]
        else:
            data["subject"] = raw["subject"]

        data["summary"] = "Received {} with subject \"{}\" on repo {}".format(
            raw["reason"], data["subject"], data["repository"].get("name", "")
        )
        super().__init__(**data)


class Event(BaseModel):
    raw: dict
    github_id: Optional[int]
    type: Optional[str]
    actor: Optional[str]
    public: Optional[bool]
    created_at: Optional[datetime]
    repo: Optional[dict]
    org: Optional[str]
    create_data: Optional[dict]
    delete_data: Optional[dict]
    issue_comment_data: Optional[dict]
    pull_request_data: Optional[dict]
    pull_request_review_comment_data: Optional[dict]
    pull_request_review_event_data: Optional[dict]
    fork_data: Optional[dict]
    push_data: Optional[dict]
    watch_data: Optional[dict]
    member_data: Optional[dict]
    summary: Optional[str]

    def __init__(self, raw) -> None:
        data = {"raw": raw}
        data["github_id"] = raw["id"]
        data["type"] = raw["type"]
        data["actor"] = raw["actor"].get("login")
        data["public"] = raw["public"]
        data["created_at"] = raw["created_at"]
        data["created_at"] = parse_datetime(data["created_at"], '%Y-%m-%dT%H:%M:%S%z')
        data["repo"] = {
            "id": raw.get("repo", {}).get("id"),
            "name": raw.get("repo", {}).get("name"),
            "url": raw.get("repo", {}).get("url"),
        }

        if raw.get("org"):
            data["org"] = raw["org"].get("login")

        if data["type"] == "CreateEvent":
            data["create_data"] = {
                "ref": raw["payload"]["ref"],
                "ref_type": raw["payload"]["ref_type"],
                "master_branch": raw["payload"]["master_branch"],
                "description": raw["payload"]["description"],
            }
            data["summary"] = "{} created {} {} on repository {} ".format(
                data["actor"],
                raw["payload"].get("ref_type", ""),
                raw["payload"].get("ref", ""),
                data["repo"]["name"]
            )
        elif data["type"] == "DeleteEvent":
            data["delete_data"] = {
                "ref": raw["payload"]["ref"],
                "ref_type": raw["payload"]["ref_type"],
                "pusher_type": raw["payload"]["pusher_type"],
            }
            data["summary"] = "{} deleted {} {} on repository {} ".format(
                data["actor"],
                raw["payload"].get("ref_type", ""),
                raw["payload"].get("ref", ""),
                data["repo"]["name"]
            )
        elif data["type"] == "IssueCommentEvent" or data["type"] == "IssuesEvent":
            created_at = raw["payload"]["issue"]["created_at"]
            if created_at:
                created_at = parse_datetime(created_at, '%Y-%m-%dT%H:%M:%S%z')

            updated_at = raw["payload"]["issue"]["updated_at"]
            if updated_at:
                updated_at = parse_datetime(updated_at, '%Y-%m-%dT%H:%M:%S%z')

            closed_at = raw["payload"]["issue"]["closed_at"]
            if closed_at:
                closed_at = parse_datetime(closed_at, '%Y-%m-%dT%H:%M:%S%z')

            assignee = raw["payload"]["issue"]["assignee"]
            data["issue_comment_data"] = {
                "action": raw["payload"]["action"],
                "issue": {
                    "number": raw["payload"]["issue"]["number"],
                    "title": raw["payload"]["issue"]["title"],
                    "url": raw["payload"]["issue"]["html_url"],
                    "user": raw["payload"]["issue"]["user"]["login"],
                    "labels": raw["payload"]["issue"]["labels"],
                    "state": raw["payload"]["issue"]["state"],
                    "assignee": assignee.get("user", {}).get("login") if assignee else assignee,
                    "assignees": [
                        user.get("login")
                        for user in raw["payload"]["issue"]["assignees"] if user
                    ],
                    "comments": raw["payload"]["issue"]["comments"],
                    "created_at": created_at,
                    "updated_at": updated_at,
                    "closed_at": closed_at,
                    "author_association": raw["payload"]["issue"]["author_association"],
                    "body": raw["payload"]["issue"]["body"],
                    "comment": raw["payload"].get("comment", {}).get("body")
                }
            }
            data["summary"] = "{} commented \"{}\" on the repository {}".format(
                data["actor"],
                raw["payload"].get("comment", {}).get("body", ""),
                data["repo"]["name"]
            )
        elif data["type"] == "PullRequestEvent":
            created_at = raw["payload"]["pull_request"]["created_at"]
            if created_at:
                created_at = parse_datetime(created_at, '%Y-%m-%dT%H:%M:%S%z')

            updated_at = raw["payload"]["pull_request"]["updated_at"]
            if updated_at:
                updated_at = parse_datetime(updated_at, '%Y-%m-%dT%H:%M:%S%z')

            closed_at = raw["payload"]["pull_request"]["closed_at"]
            if closed_at:
                closed_at = parse_datetime(closed_at, '%Y-%m-%dT%H:%M:%S%z')

            merged_at = raw["payload"]["pull_request"]["merged_at"]
            if merged_at:
                merged_at = parse_datetime(merged_at, '%Y-%m-%dT%H:%M:%S%z')

            assignee = raw["payload"]["pull_request"]["assignee"]
            data["pull_request_data"] = {
                "action": raw["payload"]["action"],
                "number": raw["payload"]["number"],
                "id": raw["payload"]["pull_request"]["id"],
                "state": raw["payload"]["pull_request"]["state"],
                "title": raw["payload"]["pull_request"]["title"],
                "body": raw["payload"]["pull_request"]["body"],
                "created_at": created_at,
                "updated_at": updated_at,
                "closed_at": closed_at,
                "merged_at": merged_at,
                "merge_commit_sha": raw["payload"]["pull_request"]["merge_commit_sha"],
                "assignee": assignee.get("user", {}).get("login") if assignee else assignee,
                "assignees": [
                    user.get("login")
                    for user in raw["payload"]["pull_request"]["assignees"] if user
                ],
                "requested_reviewers": [
                    user.get("login")
                    for user in raw["payload"]["pull_request"]["requested_reviewers"] if user
                ],
                "requested_teams": [
                    user.get("login")
                    for user in raw["payload"]["pull_request"]["requested_teams"] if user
                ],
                "labels": raw["payload"]["pull_request"]["labels"],
                "draft": raw["payload"]["pull_request"]["draft"],
                "head_ref": raw["payload"]["pull_request"].get("head", {}).get("label"),
                "head_sha": raw["payload"]["pull_request"].get("head", {}).get("sha"),
                "base_ref": raw["payload"]["pull_request"].get("base", {}).get("label"),
                "base_sha": raw["payload"]["pull_request"].get("base", {}).get("sha"),
                "author_association": raw["payload"]["pull_request"]["author_association"],
                "merged": raw["payload"]["pull_request"]["merged"],
                "merged_by": raw["payload"]["pull_request"]["merged_by"],
                "comments": raw["payload"]["pull_request"]["comments"],
                "review_comments": raw["payload"]["pull_request"]["review_comments"],
                "maintainer_can_modify": raw["payload"]["pull_request"]["maintainer_can_modify"],
                "commits": raw["payload"]["pull_request"]["commits"],
                "additions": raw["payload"]["pull_request"]["additions"],
                "deletions": raw["payload"]["pull_request"]["deletions"],
                "changed_files": raw["payload"]["pull_request"]["changed_files"],
            }
            data["summary"] = "{} {} a PR {} on the repository {}".format(
                data["actor"],
                raw["payload"]["action"],
                raw["payload"]["pull_request"]["title"],
                data["repo"]["name"]
            )
        elif data["type"] == "PullRequestReviewCommentEvent":
            created_at = raw["payload"].get("comment", {}).get("created_at")
            if created_at:
                created_at = parse_datetime(created_at, '%Y-%m-%dT%H:%M:%S%z')

            updated_at = raw["payload"].get("comment", {}).get("updated_at")
            if updated_at:
                updated_at = parse_datetime(updated_at, '%Y-%m-%dT%H:%M:%S%z')

            data["pull_request_review_comment_data"] = {
                "action": raw["payload"]["action"],
                "comment": {
                    "user": raw["payload"].get("comment", {}).get("user", {}).get("login"),
                    "diff_hunk": raw["payload"].get("comment", {}).get("diff_hunk"),
                    "body": raw["payload"].get("comment", {}).get("body"),
                    "created_at": created_at,
                    "updated_at": updated_at,
                    "author_association": raw["payload"].get("comment", {}).get("author_association")
                },
            }

            created_at = raw["payload"]["pull_request"]["created_at"]
            if created_at:
                created_at = parse_datetime(created_at, '%Y-%m-%dT%H:%M:%S%z')

            updated_at = raw["payload"]["pull_request"]["updated_at"]
            if updated_at:
                updated_at = parse_datetime(updated_at, '%Y-%m-%dT%H:%M:%S%z')

            closed_at = raw["payload"]["pull_request"]["closed_at"]
            if closed_at:
                closed_at = parse_datetime(closed_at, '%Y-%m-%dT%H:%M:%S%z')

            merged_at = raw["payload"]["pull_request"]["merged_at"]
            if merged_at:
                merged_at = parse_datetime(merged_at, '%Y-%m-%dT%H:%M:%S%z')

            assignee = raw["payload"]["pull_request"]["assignee"]
            data["pull_request_review_comment_data"]["pull_request"] = {
                "number": raw["payload"]["pull_request"]["number"],
                "state": raw["payload"]["pull_request"]["state"],
                "title": raw["payload"]["pull_request"]["title"],
                "body": raw["payload"]["pull_request"]["body"],
                "user": raw["payload"]["pull_request"]["user"]["login"],
                "created_at": created_at,
                "updated_at": updated_at,
                "closed_at": closed_at,
                "merged_at": merged_at,
                "merge_commit_sha": raw["payload"]["pull_request"]["merge_commit_sha"],
                "assignee": assignee.get("user", {}).get("login") if assignee else assignee,
                "assignees": [
                    user.get("login")
                    for user in raw["payload"]["pull_request"]["assignees"] if user
                ],
                "requested_reviewers": [
                    user.get("login")
                    for user in raw["payload"]["pull_request"]["requested_reviewers"] if user
                ],
                "requested_teams": [
                    user.get("login")
                    for user in raw["payload"]["pull_request"]["requested_teams"] if user
                ],
                "labels": raw["payload"]["pull_request"]["labels"],
                "comment": raw["payload"].get("comment", {}).get("body", ""),
                "url": raw["payload"].get("comment", {}).get("html_url", ""),
                "draft": raw["payload"]["pull_request"]["draft"],
                "head_ref": raw["payload"]["pull_request"].get("head", {}).get("label"),
                "head_sha": raw["payload"]["pull_request"].get("head", {}).get("sha"),
                "base_ref": raw["payload"]["pull_request"].get("base", {}).get("label"),
                "base_sha": raw["payload"]["pull_request"].get("base", {}).get("sha"),
                "author_association": raw["payload"]["pull_request"]["author_association"],
            }
            data["summary"] = "{} left a comment on PR #{} on the repository {}".format(
                data["actor"],
                raw["payload"]["pull_request"]["number"],
                data["repo"]["name"]
            )
        elif data["type"] == "PullRequestReviewEvent":
            submitted_at = raw["payload"].get("review", {}).get("submitted_at")
            if submitted_at:
                submitted_at = parse_datetime(submitted_at, '%Y-%m-%dT%H:%M:%S%z')

            created_at = raw["payload"]["pull_request"]["created_at"]
            if created_at:
                created_at = parse_datetime(created_at, '%Y-%m-%dT%H:%M:%S%z')

            updated_at = raw["payload"]["pull_request"]["updated_at"]
            if updated_at:
                updated_at = parse_datetime(updated_at, '%Y-%m-%dT%H:%M:%S%z')

            closed_at = raw["payload"]["pull_request"]["closed_at"]
            if closed_at:
                closed_at = parse_datetime(closed_at, '%Y-%m-%dT%H:%M:%S%z')

            merged_at = raw["payload"]["pull_request"]["merged_at"]
            if merged_at:
                merged_at = parse_datetime(merged_at, '%Y-%m-%dT%H:%M:%S%z')

            assignee = raw["payload"]["pull_request"]["assignee"]
            data["pull_request_review_event_data"] = {
                "action": raw["payload"]["action"],
                "review": {
                    "user": raw["payload"].get("review", {}).get("user", {}).get("login"),
                    "body": raw["payload"].get("review", {}).get("body"),
                    "submitted_at": submitted_at,
                    "state": raw["payload"].get("review", {}).get("state"),
                    "author_association": raw["payload"].get("review", {}).get("author_association"),
                },
                "pull_request": {
                    "number": raw["payload"]["pull_request"]["number"],
                    "state": raw["payload"]["pull_request"]["state"],
                    "title": raw["payload"]["pull_request"]["title"],
                    "body": raw["payload"]["pull_request"]["body"],
                    "user": raw["payload"]["pull_request"]["user"]["login"],
                    "created_at": created_at,
                    "updated_at": updated_at,
                    "closed_at": closed_at,
                    "merged_at": merged_at,
                    "merge_commit_sha": raw["payload"]["pull_request"]["merge_commit_sha"],
                    "assignee": assignee.get("user", {}).get("login") if assignee else assignee,
                    "assignees": [
                        user.get("login")
                        for user in raw["payload"]["pull_request"]["assignees"] if user
                    ],
                    "requested_reviewers": [
                        user.get("login")
                        for user in raw["payload"]["pull_request"]["requested_reviewers"] if user
                    ],
                    "requested_teams": [
                        user.get("login")
                        for user in raw["payload"]["pull_request"]["requested_teams"] if user
                    ],
                    "labels": raw["payload"]["pull_request"]["labels"],
                    "draft": raw["payload"]["pull_request"]["draft"],
                    "head_ref": raw["payload"]["pull_request"].get("head", {}).get("label"),
                    "head_sha": raw["payload"]["pull_request"].get("head", {}).get("sha"),
                    "base_ref": raw["payload"]["pull_request"].get("base", {}).get("label"),
                    "base_sha": raw["payload"]["pull_request"].get("base", {}).get("sha"),
                    "author_association": raw["payload"]["pull_request"]["author_association"],
                }
            }
            data["summary"] = "{} marked PR #{} as {} on the repository {}".format(
                data["actor"],
                raw["payload"]["pull_request"]["number"],
                raw["payload"]["pull_request"]["state"],
                data["repo"]["name"]
            )
        elif data["type"] == "PushEvent":
            data["push_data"] = {
                "ref": raw.get("payload", {}).get("ref"),
                "commits": [
                    commit["message"]
                    for commit in raw.get("payload", {}).get("commits", []) if commit
                ],
            }
            data["summary"] = "{} pushed to {} on the repository {}".format(
                data["actor"],
                raw.get("payload", {}).get("ref"),
                data["repo"]["name"]
            )
        elif data["type"] == "WatchEvent":
            data["watch_data"] = {
                "action": raw.get("payload", {}).get("action"),
            }
            data["summary"] = "{} started to watch {} on github".format(data["actor"], data["repo"]["name"])
        elif data["type"] == "ForkEvent":
            forkee = raw.get("payload", {}).get("forkee")
            data["fork_data"] = {
                "name": forkee.get("name"),
                "full_name": forkee.get("full_name"),
                "url": forkee.get("html_url")
            }
            data["summary"] = "{} forked {} on github".format(data["actor"], data["repo"]["name"])
        elif data["type"] == "MemberEvent":
            member = raw.get("payload", {}).get("member")
            data["member_data"] = {
                "action": raw.get("payload", {}).get("action"),
                "login": member.get("login"),
                "url": member.get("html_url"),
            }
            data["summary"] = "{} {} {} to {}".format(
                data["actor"], raw.get("payload", {}).get("action"), member.get("login"), data["repo"]["name"]
            )
        elif data["type"] == "PublicEvent":
            data["summary"] = "{} triggered a public event on {}".format(data["actor"], data["repo"]["name"])
        else:
            print("New event, you need to change the processing module and the importers", data["type"])

        super().__init__(**data)


def _fetch_details():
    details = {}
    files = get_notification_detail_file_paths()

    for file in files:
        with open(file, 'r') as json_file:
            content = json.load(json_file)
            details.update(content)
    return details


def process_notifications(input_files=None, use_details=True):
    if not input_files:
        input_files = get_notification_file_paths()

    details = None
    handled = set()
    if use_details:
        details = _fetch_details()

    for file in input_files:
        with open(file, 'r') as json_file:
            content = json.load(json_file)
            for notification in content:
                id = notification["id"]
                if id in handled:
                    continue
                else:
                    handled.add(id)
                    yield Notification(notification, details)


def process_events(input_files=None):
    if not input_files:
        input_files = get_events_file_paths()

    handled = set()
    for file in input_files:
        with open(file, 'r') as json_file:
            content = json.load(json_file)
            for event in content:
                id = event["id"]
                if id in handled:
                    continue
                else:
                    handled.add(id)
                    yield Event(raw=event)

