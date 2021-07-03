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
        }


def process_moods(data_iterable=None):
    print("Processing moods")
    if not data_iterable:
        data_iterable = []

    for mood in data_iterable:
        yield {
            "provider": mood.provider,
            "activity": "rated",
            "principal_entity": "Rebeca Sarai",
            "activity_entities": ["day"],
            "datetime": mood.date_tz,
            "details": mood.note,
            "mood": mood.mood,
            "things_i_did": mood.things_i_did,
            "timestamp_utc": str(mood.date_tz.astimezone(pytz.utc).timestamp()),
            "timezone": "America/Recife",
            "device_name": "Galaxy S10",
        }


def process_google_chrome(data_iterable=None):
    print("Processing browser history, this will take a while")
    if not data_iterable:
        data_iterable = []

    for link in data_iterable:
        yield {
            "provider": link.provider,
            "activity": "accessed",
            "principal_entity": "Rebeca Sarai",
            "activity_entities": ["site"],
            "datetime": link.date_tz,
            "timestamp_utc": str(link.date_tz.astimezone(pytz.utc).timestamp()),
            "timezone": "America/Recife",
            "device_name": "Avell G1711: rsarai",
            "website_title": link.title,
            "website_url": link.url,
            "visit_count": link.visit_count,
            "typed_count": link.typed_count,
            "hidden": link.hidden,
            "transition": link.transition,
            "publicly_routable": link.publicly_routable,
        }


def process_toggl(data_iterable=None):
    print("Processing toggl")
    if not data_iterable:
        data_iterable = []

    for entry in data_iterable:
        activity_entities = [entry.project_name.lower()] if entry.project_name else []
        yield {
            "provider": "toggl",
            "activity": "tracked",
            "principal_entity": "Rebeca Sarai",
            "activity_entities": activity_entities,
            "datetime": entry.stop,
            "timestamp_utc": str(entry.at.astimezone(pytz.utc).timestamp()),
            "timezone": "America/Recife",
            "device_name": "Web App",
            "start": entry.start,
            "duration": entry.duration,
            "description": entry.description,
            "duronly": entry.duronly,
            "tags": entry.tags,
            "at": entry.at,
            "project_name": entry.project_name,
            "project_id": entry.project_id,
            "project_is_active": entry.project_is_active,
        }


def process_rescue_time_summary(data_iterable=None):
    print("Processing rescuetime daily summary")
    if not data_iterable:
        data_iterable = []

    for summary in data_iterable:
        yield {
            "provider": "rescuetime",
            "activity": "generated",
            "principal_entity": "Rebeca Sarai",
            "activity_entities": [],
            "datetime": summary.datetime,
            "timestamp_utc": str(summary.datetime.astimezone(pytz.utc).timestamp()),
            "timezone": "America/Recife",
            "device_name": "Web App",
            "productivity_pulse": summary.productivity_pulse,
            "very_productive_percentage": summary.very_productive_percentage,
            "productive_percentage": summary.productive_percentage,
            "neutral_percentage": summary.neutral_percentage,
            "distracting_percentage": summary.distracting_percentage,
            "very_distracting_percentage": summary.very_distracting_percentage,
            "all_productive_percentage": summary.all_productive_percentage,
            "all_distracting_percentage": summary.all_distracting_percentage,
            "uncategorized_percentage": summary.uncategorized_percentage,
            "business_percentage": summary.business_percentage,
            "communication_and_scheduling_percentage": summary.communication_and_scheduling_percentage,
            "social_networking_percentage": summary.social_networking_percentage,
            "design_and_composition_percentage": summary.design_and_composition_percentage,
            "entertainment_percentage": summary.entertainment_percentage,
            "news_percentage": summary.news_percentage,
            "software_development_percentage": summary.software_development_percentage,
            "reference_and_learning_percentage": summary.reference_and_learning_percentage,
            "shopping_percentage": summary.shopping_percentage,
            "utilities_percentage": summary.utilities_percentage,
            "total_hours": summary.total_hours,
            "very_productive_hours": summary.very_productive_hours,
            "productive_hours": summary.productive_hours,
            "neutral_hours": summary.neutral_hours,
            "distracting_hours": summary.distracting_hours,
            "very_distracting_hours": summary.very_distracting_hours,
            "all_productive_hours": summary.all_productive_hours,
            "all_distracting_hours": summary.all_distracting_hours,
            "uncategorized_hours": summary.uncategorized_hours,
            "business_hours": summary.business_hours,
            "communication_and_scheduling_hours": summary.communication_and_scheduling_hours,
            "social_networking_hours": summary.social_networking_hours,
            "design_and_composition_hours": summary.design_and_composition_hours,
            "entertainment_hours": summary.entertainment_hours,
            "news_hours": summary.news_hours,
            "software_development_hours": summary.software_development_hours,
            "reference_and_learning_hours": summary.reference_and_learning_hours,
            "shopping_hours": summary.shopping_hours,
            "utilities_hours": summary.utilities_hours,
            "total_duration_formatted": summary.total_duration_formatted,
            "very_productive_duration_formatted": summary.very_productive_duration_formatted,
            "productive_duration_formatted": summary.productive_duration_formatted,
            "neutral_duration_formatted": summary.neutral_duration_formatted,
            "distracting_duration_formatted": summary.distracting_duration_formatted,
            "very_distracting_duration_formatted": summary.very_distracting_duration_formatted,
            "all_productive_duration_formatted": summary.all_productive_duration_formatted,
            "all_distracting_duration_formatted": summary.all_distracting_duration_formatted,
            "uncategorized_duration_formatted": summary.uncategorized_duration_formatted,
            "business_duration_formatted": summary.business_duration_formatted,
            "communication_and_scheduling_duration_formatted": summary.communication_and_scheduling_duration_formatted,
            "social_networking_duration_formatted": summary.social_networking_duration_formatted,
            "design_and_composition_duration_formatted": summary.design_and_composition_duration_formatted,
            "entertainment_duration_formatted": summary.entertainment_duration_formatted,
            "news_duration_formatted": summary.news_duration_formatted,
            "software_development_duration_formatted": summary.software_development_duration_formatted,
            "reference_and_learning_duration_formatted": summary.reference_and_learning_duration_formatted,
            "shopping_duration_formatted": summary.shopping_duration_formatted,
            "utilities_duration_formatted": summary.utilities_duration_formatted,
        }


def process_rescue_time_analytics(data_iterable=None):
    print("Processing rescuetime analytics")
    if not data_iterable:
        data_iterable = []

    for entry in data_iterable:
        yield {
            "provider": "rescuetime",
            "activity": "tracked",
            "principal_entity": "Rebeca Sarai",
            "activity_entities": ['site'],
            "datetime": entry.datetime,
            "timestamp_utc": str(entry.datetime.astimezone(pytz.utc).timestamp()),
            "timezone": "America/Recife",
            "device_name": "Web App",
            "time_spent_in_seconds": entry.time_spent_in_seconds,
            "number_of_people": entry.number_of_people,
            "detail": entry.detail,
            "category": entry.category,
            "productivity": entry.productivity,
        }


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
        data["activity_entities"] = ["credit card event"]
        data["device_name"] = "Rebeca's account"
        data["timestamp_utc"] = str(event.date_tz.astimezone(pytz.utc).timestamp()),
        data["datetime"] = event.date_tz
        data["timezone"] = "America/Recife"
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
        data["activity_entities"] = ["account event"]
        data["device_name"] = "Rebeca's account"
        data["timestamp_utc"] = str(event.date_tz.astimezone(pytz.utc).timestamp()),
        data["datetime"] = event.date_tz
        data["timezone"] = "America/Recife"
        yield data


def process_nubank_bills(data_iterable=None):
    print("Processing nubank bill details")
    if not data_iterable:
        data_iterable = []

    for event in data_iterable:
        data = event.dict()
        data["provider"] = "nubank"
        data["activity"] = "triggered"
        data["principal_entity"] = "Rebeca Sarai"
        data["activity_entities"] = ["bill purchases"]
        data["device_name"] = "Rebeca's account"
        data["timestamp_utc"] = str(event.close_date.astimezone(pytz.utc).timestamp()),
        data["datetime"] = event.close_date
        data["timezone"] = "America/Recife"
        yield data
