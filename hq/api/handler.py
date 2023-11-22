import pytz
from datetime import datetime


def process_bash(data_iterable=None):
    print("Processing bash commands")
    if not data_iterable:
        data_iterable = []

    for cmd in data_iterable:
        if "ls" in cmd.cmd or "cd .." in cmd.cmd:
            continue

        timestamp_utc = str(cmd.date_tz.astimezone(pytz.utc).timestamp()) if cmd.date_tz else None
        data = cmd.dict()
        data["provider"] = "bash"
        data["activity"] = "commanded"
        data["principal_entity"] = "Rebeca Sarai"
        data["activity_entities"] = []
        data["timezone"] = "America/Recife"
        data["datetime"] = cmd.date_tz
        data["timestamp_utc"] = timestamp_utc
        data["command"] = cmd.cmd
        data["folder"] = cmd.folder
        data["device_name"] = cmd.host
        data["summary"] = f"Used command \"{cmd.cmd}\" on host: {cmd.host}"
        del data["date_tz"]
        yield data


def process_habits(data_iterable=None):
    print("Processing habits")
    if not data_iterable:
        data_iterable = []

    for habit in data_iterable:
        data = habit.dict()
        data["provider"] = "habits"
        data["activity"] = "marked"
        data["principal_entity"] = "Rebeca Sarai"
        data["activity_entities"] = [habit.name.lower()]
        data["timezone"] = "America/Recife"
        data["device_name"] = "Galaxy S10"
        data["datetime"] = habit.date_tz
        data["timestamp_utc"] = str(habit.date_tz.astimezone(pytz.utc).timestamp())
        data["detail"] = habit.description
        data["summary"] = f"Marked YES to \"{habit.description}\" on habits"
        yield data


def process_moods(data_iterable=None):
    print("Processing moods")
    if not data_iterable:
        data_iterable = []

    for mood in data_iterable:
        data = mood.dict()
        data["provider"] = "daylio"
        data["activity"] = "rated"
        data["principal_entity"] = "Rebeca Sarai"
        data["activity_entities"] = ["day"]
        data["datetime"] = mood.date_tz
        data["timestamp_utc"] = str(mood.date_tz.astimezone(pytz.utc).timestamp())
        data["timezone"] = "America/Recife"
        data["device_name"] = "Galaxy S10"
        data["summary"] = f"Rated the day as {mood.mood} and did \"{mood.things_i_did}\" on daylio"
        del data["date_tz"]
        yield data


def process_google_chrome(data_iterable=None):
    print("Processing browser history, this will take a while")
    if not data_iterable:
        data_iterable = []

    for link in data_iterable:
        data = link.dict()
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
        data["summary"] = f"Accessed \"{link.title}\" on google chrome"
        del data["raw"]
        del data["title"]
        del data["url"]
        del data["date_tz"]
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
        data["summary"] = "Clocked {} doing {} on project \"{}\"".format(
            entry.human_time_duration,
            entry.description,
            entry.project_name
        )
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
        data["summary"] = "Clocked {} and out of that {} were very productive".format(
            summary.total_duration_formatted,
            summary.very_productive_duration_formatted
        )
        yield data


def process_rescue_time_analytics(data_iterable=None):
    print("Processing rescuetime analytics")
    if not data_iterable:
        data_iterable = []

    for entry in data_iterable:
        data = entry.dict()
        data["provider"] = "rescuetime"
        data["activity"] = "tracked"
        data["principal_entity"] = "Rebeca Sarai"
        data["activity_entities"] = ['site']
        data["datetime"] = entry.date_tz
        data["timestamp_utc"] = str(entry.date_tz.astimezone(pytz.utc).timestamp())
        data["timezone"] = "America/Recife"
        data["device_name"] = "Web App"
        data["summary"] = f"Entry on rescue time. {entry.time_spent_in_seconds} seconds spent on {entry.detail}"
        del data["raw"]
        yield data


def process_github_notifications(data_iterable=None):
    print("Processing github notifications")
    if not data_iterable:
        data_iterable = []

    for notification in data_iterable:
        data = notification.dict()
        data["provider"] = "github"
        data["activity"] = "received"
        data["principal_entity"] = "Rebeca Sarai"
        data["activity_entities"] = ["notification"]
        data["timestamp_utc"] = str(notification.updated_at.astimezone(pytz.utc).timestamp())
        data["timezone"] = "America/Recife"
        data["device_name"] = "rsarai account"
        data["summary"] = notification.summary
        yield data


def process_github_events(data_iterable=None):
    print("Processing github events")
    if not data_iterable:
        data_iterable = []

    for event in data_iterable:
        data = event.dict()
        data["provider"] = "github"
        data["activity"] = "triggered"
        data["principal_entity"] = "Rebeca Sarai"
        data["activity_entities"] = [event.type.lower()]
        data["datetime"] = event.created_at
        data["timestamp_utc"] = str(event.created_at.astimezone(pytz.utc).timestamp())
        data["timezone"] = "America/Recife"
        data["device_name"] = "rsarai's account"
        data["summary"] = event.summary
        yield data


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
        data["summary"] = f"Transaction on nubank card feed: {event.description} R${event.amount}"
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
        event.detail
        data["summary"] = f"Nubank generic feed event: {event.title} {event.detail}"
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
        data["summary"] = f"Bill processed by Nubank with the value of R${event.total_balance}"
        del data["raw"]
        yield data


def process_wakatime(data_iterable=None):
    print("Processing wakatime stats")
    if not data_iterable:
        data_iterable = []

    for event in data_iterable:
        data = event.dict()
        data["provider"] = "wakatime"
        data["activity"] = "tracked"
        data["principal_entity"] = "Rebeca Sarai"
        data["activity_entities"] = []
        data["timezone"] = "America/Recife"
        data["timestamp_utc"] = str(event.date_tz.astimezone(pytz.utc).timestamp()),
        data["datetime"] = event.date_tz
        projects = ", ".join([p.get("name") for p in event.projects])
        grand_total = event.grand_total.get("text")
        data["summary"] = f"Tracked {grand_total} through wakatime working on {projects}"
        del data["raw"]
        yield data


def process_google_takeout_calendar(data_iterable=None):
    print("Processing google takeout calendar stats")
    if not data_iterable:
        data_iterable = []

    for calendar in data_iterable:
        data = calendar.dict()
        data["provider"] = "google takeout calendar"
        data["activity"] = "participated"
        data["principal_entity"] = "Rebeca Sarai"
        data["activity_entities"] = ["meeting"]
        data["timezone"] = "America/Recife"
        data["timestamp_utc"] = str(calendar.begin.astimezone(pytz.utc).timestamp()),
        data["datetime"] = calendar.begin
        data["summary"] = f"Participated in the a \"{calendar.name}\" meeting"
        del data["raw"]
        del data["tz"]
        del data["attendees"]
        del data["categories"]
        del data["alarms"]

        keys_to_delete = []
        for key, value in data.items():
            if isinstance(value, datetime):
                keys_to_delete.append(key)
        for key in keys_to_delete:
            del data[key]

        yield data


def process_google_takeout_maps_semantic_locations(data_iterable=None):
    print("Processing google takeout maps stats")
    if not data_iterable:
        data_iterable = []

    for entry in data_iterable:
        data = entry.dict()
        data["provider"] = "google takeout maps"
        data["activity"] = "visited"
        data["principal_entity"] = "Rebeca Sarai"
        data["activity_entities"] = ["location"]
        data["timestamp_utc"] = str(entry.date_tz.astimezone(pytz.utc).timestamp()),
        data["datetime"] = entry.date_tz
        data["latitude"] = entry.latitudeE7 / 10_000_000 if entry.latitudeE7 else None
        data["longitude"] = entry.longitudeE7  / 10_000_000 if entry.longitudeE7 else None
        data["summary"] = f"Stayed on \"{entry.name}\" (full address: {entry.address})"
        del data["raw"]

        keys_to_delete = []
        for key, value in data.items():
            if isinstance(value, datetime):
                keys_to_delete.append(key)
        for key in keys_to_delete:
            del data[key]

        yield data


def process_google_takeout_my_activity(data_iterable=None):
    print("Processing google takeout my activity stats")
    if not data_iterable:
        data_iterable = []

    for entry in data_iterable:
        data = entry.dict()
        data["provider"] = "google takeout my activity"
        data["activity"] = "engaged"
        data["principal_entity"] = "Rebeca Sarai"
        data["activity_entities"] = ["activity"]
        data["timestamp_utc"] = str(entry.date_tz.astimezone(pytz.utc).timestamp()),
        data["datetime"] = entry.date_tz
        data["summary"] = f"Engaged with {entry.title} and {entry.content}"
        del data["raw"]

        keys_to_delete = []
        for key, value in data.items():
            if isinstance(value, datetime):
                keys_to_delete.append(key)
        for key in keys_to_delete:
            del data[key]

        yield data


def process_google_takeout_play_store(data_iterable=None):
    print("Processing google takeout play store stats")
    if not data_iterable:
        data_iterable = []

    for entry in data_iterable:
        data = entry.dict()
        data["provider"] = "play store"
        data["activity"] = "engaged"
        data["principal_entity"] = "Rebeca Sarai"
        data["activity_entities"] = ["play store"]
        if hasattr(entry, "date_tz") and getattr(entry, "date_tz"):
            data["timestamp_utc"] = str(entry.date_tz.astimezone(pytz.utc).timestamp()),
            data["datetime"] = entry.date_tz
            del data["date_tz"]
        data["summary"] = f"Interacted with {entry.description} \"{entry.title}\""

        del data["raw"]

        keys_to_delete = []
        for key, value in data.items():
            if isinstance(value, datetime):
                keys_to_delete.append(key)
        for key in keys_to_delete:
            del data[key]

        yield data
