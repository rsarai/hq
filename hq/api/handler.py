import pytz


def process_bash(data_iterable=None):
    print("Processing bash commands")
    if not data_iterable:
        data_iterable = []

    for cmd in data_iterable:
        if "ls" in cmd.cmd or "cd .." in cmd.cmd:
            continue

        timestamp_utc = str(cmd.date_tz.astimezone(pytz.utc).timestamp()) if cmd.date_tz else None
        yield {
            "provider": "bash",
            "activity": "commanded",
            "principal_entity": "Rebeca Sarai",
            "activity_entities": [],
            "datetime": cmd.date_tz,
            "timestamp_utc": timestamp_utc,
            "timezone": "America/Recife",
            "command": cmd.cmd,
            "folder": cmd.folder,
            "device_name": cmd.host,
        }


def process_habits(data_iterable=None):
    print("Processing habits")
    if not data_iterable:
        data_iterable = []

    for habit in data_iterable:
        yield {
            "provider": "habits",
            "activity": "marked",
            "principal_entity": "Rebeca Sarai",
            "activity_entities": [habit.name.lower()],
            "datetime": habit.date_tz,
            "timestamp_utc": str(habit.date_tz.astimezone(pytz.utc).timestamp()),
            "timezone": "America/Recife",
            "device_name": "Galaxy S10",
            "detail": habit.description,
        }


def process_moods(data_iterable=None):
    print("Processing moods")
    if not data_iterable:
        data_iterable = []

    for mood in data_iterable:
        data = mood.dict()
        del data["date_tz"]
        data["provider"] = "daylio",
        data["activity"] = "rated",
        data["principal_entity"] = "Rebeca Sarai",
        data["activity_entities"] = ["day"],
        data["datetime"] = mood.date_tz,
        data["timestamp_utc"] = str(mood.date_tz.astimezone(pytz.utc).timestamp()),
        data["timezone"] = "America/Recife",
        data["device_name"] = "Galaxy S10",
        yield data


def process_google_chrome(data_iterable=None):
    print("Processing browser history, this will take a while")
    if not data_iterable:
        data_iterable = []

    for link in data_iterable:
        data = link.dict()
        del data["raw"]
        del data["title"]
        del data["url"]
        del data["date_tz"]
        data["provider"] = "google chrome"
        data["activity"] = "accessed"
        data["principal_entity"] = "Rebeca Sarai"
        data["activity_entities"] = ["site"]
        data["datetime"] = link.date_tz
        data["timestamp_utc"] = str(link.date_tz.astimezone(pytz.utc).timestamp())
        data["timezone"] = "America/Recife"
        data["device_name"] = "Avell G1711: rsarai"
        data["website_title"] = link.title
        data["website_url"] = link.url
        yield data


def process_toggl(data_iterable=None):
    print("Processing toggl")
    if not data_iterable:
        data_iterable = []

    for entry in data_iterable:
        data = entry.dict()
        activity_entities = [entry.project_name.lower()] if entry.project_name else []
        del data["raw"]
        data["provider"] = "toggl"
        data["activity"] = "tracked"
        data["principal_entity"] = "Rebeca Sarai"
        data["activity_entities"] = activity_entities
        data["datetime"] = entry.at
        data["timestamp_utc"] = str(entry.at.astimezone(pytz.utc).timestamp())
        data["timezone"] = "America/Recife"
        data["device_name"] = "Web App"
        yield data


def process_rescue_time_summary(data_iterable=None):
    print("Processing rescuetime daily summary")
    if not data_iterable:
        data_iterable = []

    for summary in data_iterable:
        data = summary.dict()
        del data["raw"]
        data["provider"] = "rescuetime"
        data["activity"] = "generated"
        data["principal_entity"] = "Rebeca Sarai"
        data["activity_entities"] = []
        data["datetime"] = summary.date_tz
        data["timestamp_utc"] = str(summary.date_tz.astimezone(pytz.utc).timestamp())
        data["timezone"] = "America/Recife"
        data["device_name"] = "Web App"
        yield data


def process_rescue_time_analytics(data_iterable=None):
    print("Processing rescuetime analytics")
    if not data_iterable:
        data_iterable = []

    for entry in data_iterable:
        data = entry.dict()
        del data["raw"]
        data["provider"] = "rescuetime"
        data["activity"] = "tracked"
        data["principal_entity"] = "Rebeca Sarai"
        data["activity_entities"] = ['site']
        data["datetime"] = entry.date_tz
        data["timestamp_utc"] = str(entry.date_tz.astimezone(pytz.utc).timestamp())
        data["timezone"] = "America/Recife"
        data["device_name"] = "Web App"
        yield data


def process_github_notifications(data_iterable=None):
    print("Processing github notifications")
    if not data_iterable:
        data_iterable = []

    for notification in data_iterable:
        yield {
            "provider": "github",
            "activity": "received",
            "principal_entity": "Rebeca Sarai",
            "activity_entities": ["notification"],
            "datetime": notification.updated_at,
            "timestamp_utc": str(notification.updated_at.astimezone(pytz.utc).timestamp()),
            "timezone": "America/Recife",
            "device_name": "rsarai account",
            "github_id": notification.github_id,
            "reason": notification.reason,
            "repository": notification.repository,
            "url": notification.url,
            "subject": notification.subject,
        }


def process_github_events(data_iterable=None):
    print("Processing github events")
    if not data_iterable:
        data_iterable = []

    for event in data_iterable:
        yield {
            "provider": "github",
            "activity": "triggered",
            "principal_entity": "Rebeca Sarai",
            "activity_entities": [event.type.lower()],
            "datetime": event.created_at,
            "timestamp_utc": str(event.created_at.astimezone(pytz.utc).timestamp()),
            "timezone": "America/Recife",
            "device_name": "rsarai's account",
            "github_id": event.github_id,
            "type": event.type,
            "public": event.public,
            "actor": event.actor,
            "org": event.org,
            "repository": event.repo,
            "created_at": event.created_at,
            "create_data": event.create_data,
            "delete_data": event.delete_data,
            "issue_comment_data": event.issue_comment_data,
            "pull_request_data": event.pull_request_data,
            "pull_request_review_comment_data": event.pull_request_review_comment_data,
            "pull_request_review_event_data": event.pull_request_review_event_data,
            "push_data": event.push_data,
            "watch_data": event.watch_data,
        }


def process_nubank_card_feed(data_iterable=None):
    print("Processing nubank card feed")
    if not data_iterable:
        data_iterable = []

    for event in data_iterable:
        data = event.dict()
        data["provider"] = "nubank"
        data["activity"] = "triggered"
        data["principal_entity"] = "Rebeca Sarai"
        data["activity_entities"] = ["charge"]
        data["device_name"] = "Rebeca's account"
        data["timestamp_utc"] = str(event.date_tz.astimezone(pytz.utc).timestamp()),
        data["datetime"] = event.date_tz
        data["timezone"] = "America/Recife"
        del data["raw"]
        yield data


def process_nubank_account_feed(data_iterable=None):
    print("Processing nubank account feed")
    if not data_iterable:
        data_iterable = []

    for event in data_iterable:
        data = event.dict()
        data["provider"] = "nubank"
        data["activity"] = "triggered"
        data["principal_entity"] = "Rebeca Sarai"
        data["activity_entities"] = ["transaction"]
        data["device_name"] = "Rebeca's account"
        data["timestamp_utc"] = str(event.date_tz.astimezone(pytz.utc).timestamp()),
        data["datetime"] = event.date_tz
        data["timezone"] = "America/Recife"
        del data["raw"]
        yield data


def process_nubank_bills(data_iterable=None):
    print("Processing nubank bill details")
    if not data_iterable:
        data_iterable = []

    for event in data_iterable:
        data = event.dict()
        data["provider"] = "nubank"
        data["activity"] = "billed"
        data["principal_entity"] = "nubank"
        data["activity_entities"] = ["Rebeca Sarai"]
        data["device_name"] = "Rebeca's account"
        data["timestamp_utc"] = str(event.close_date.astimezone(pytz.utc).timestamp()),
        data["datetime"] = event.close_date
        data["timezone"] = "America/Recife"
        del data["raw"]
        yield data
