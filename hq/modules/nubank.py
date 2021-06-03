import json
import pytz
import sys

from datetime import datetime

sys.path.append('/home/sarai/github-projects/hq')
from hq.common import get_files
from hq.config import Nubank as config


timezone = pytz.timezone("America/Recife")


class CardFeedEvent:
    def __init__(self, raw):
        if raw.get("account"):
            del raw["account"]

        if raw.get("account"):
            del raw["href"]

        if raw.get("_links"):
            del raw["_links"]

        if raw.get("tokenized"):
            del raw["tokenized"]
        del raw["id"]

        self.raw = raw
        self.description = raw.get("description")
        self.category = raw["category"]
        self.title = raw["title"]

        time = raw["time"]
        if '.' in time:
            self.date_tz = datetime.strptime(time, "%Y-%m-%dT%H:%M:%S.%fZ").replace(tzinfo=timezone)
        else:
            self.date_tz = datetime.strptime(time, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone)

        if raw.get("amount"):
            self.amount = round(float(raw["amount"]), 2)

        if raw.get("amount_without_iof"):
            self.amount_without_iof = round(float(raw["amount_without_iof"]), 2)


class Bills:
    def __init__(self, raw):
        self.raw = raw
        self.paid = round(float(raw["paid"]), 2)
        self.interest = round(float(raw["interest"]), 2)
        self.past_balance = round(float(raw["past_balance"]), 2)
        self.total_balance = round(float(raw["total_balance"]), 2)
        self.interest_rate = round(float(raw["interest_rate"]), 2)
        self.minimum_payment = round(float(raw["minimum_payment"]), 2)
        self.total_cumulative = round(float(raw["total_cumulative"]), 2)

        if raw.get("remaining_balance"):
            self.remaining_balance = round(float(raw["remaining_balance"]), 2)

        if raw.get("remaining_minimum_payment"):
            self.remaining_minimum_payment = round(float(raw["remaining_minimum_payment"]), 2)

        due_date = raw["due_date"]
        self.due_date = datetime.strptime(due_date, "%Y-%m-%d").replace(tzinfo=timezone)

        open_date = raw["open_date"]
        self.open_date = datetime.strptime(open_date, "%Y-%m-%d").replace(tzinfo=timezone)

        close_date = raw["close_date"]
        self.close_date = datetime.strptime(close_date, "%Y-%m-%d").replace(tzinfo=timezone)

        effective_due_date = raw["effective_due_date"]
        self.effective_due_date = datetime.strptime(effective_due_date, "%Y-%m-%d").replace(tzinfo=timezone)


class AccountEvent:
    def __init__(self, raw):
        del raw["id"]
        self.typename = raw["__typename"]
        self.title = raw["title"]
        self.detail = raw["detail"]

        postDate = raw["postDate"]
        self.date_tz = datetime.strptime(postDate, "%Y-%m-%d").replace(tzinfo=timezone)

        self.amount = raw["amount"]

        if raw.get("originAccount"):
            self.origin_account = raw["originAccount"]

        if raw.get("destinationAccount"):
            self.destination_account = raw["destinationAccount"]


def process_card_feed():
    card_feed_file = max(get_files(config.export_path, '*/card_feed.json'))
    card_feed_data = json.loads(card_feed_file.read_bytes())
    for event in card_feed_data["events"]:
        yield CardFeedEvent(raw=event)


def process_card_statements():
    card_statements_file = max(get_files(config.export_path, '*/card_statements.json'))
    card_statements_data = json.loads(card_statements_file.read_bytes())
    for event in card_statements_data:
        yield CardFeedEvent(raw=event)


def process_bills():
    bills_file = max(get_files(config.export_path, '*/bills.json'))
    bills_data = json.loads(bills_file.read_bytes())
    for event in bills_data:
        if 'overdue' == event.get("state"):
            yield Bills(raw=event.get("summary"))


def process_account_feed():
    account_feed_file = max(get_files(config.export_path, '*/account_feed.json'))
    account_feed_data = json.loads(account_feed_file.read_bytes())
    for event in account_feed_data:
        yield AccountEvent(raw=event)


def process_account_statements():
    account_statements_file = max(get_files(config.export_path, '*/account_statements.json'))
    account_statements_data = json.loads(account_statements_file.read_bytes())
    for event in account_feed_data:
        yield AccountEvent(raw=event)


def process_bill_details():
    bill_detail_files = get_files(config.export_path, '*/*bill-detail.json')
    for bill_file in bill_detail_files:
        bill_data = json.loads(bill_file.read_bytes())
        bill = bill_data["bill"]

        summary = bill.get("summary")
        line_items = bill.get("line_items")


# process()
