import json
from typing import Optional
import pytz

from datetime import datetime
from pydantic import BaseModel

from hq.common import get_files
from hq.config import Nubank as config


timezone = pytz.timezone("America/Recife")


class CardFeedEvent(BaseModel):
    raw: dict
    description: Optional[str]
    category: Optional[str]
    title: Optional[str]
    date_tz: Optional[datetime]
    amount: Optional[float]
    amount_without_iof: Optional[float]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if self.raw.get("account"):
            del self.raw["account"]

        if self.raw.get("account"):
            del self.raw["href"]

        if self.raw.get("_links"):
            del self.raw["_links"]

        if self.raw.get("tokenized"):
            del self.raw["tokenized"]
        del self.raw["id"]

        self.description = self.raw.get("description")
        self.category = self.raw["category"]
        self.title = self.raw["title"]

        time = self.raw["time"]
        if '.' in time:
            self.date_tz = datetime.strptime(time, "%Y-%m-%dT%H:%M:%S.%fZ").replace(tzinfo=timezone)
        else:
            self.date_tz = datetime.strptime(time, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone)

        if self.raw.get("amount"):
            self.amount = round(float(self.raw["amount"]), 2)

        if self.raw.get("amount_without_iof"):
            self.amount_without_iof = round(float(self.raw["amount_without_iof"]), 2)


class Bills(BaseModel):
    raw: dict
    paid: Optional[float]
    interest: Optional[float]
    past_balance: Optional[float]
    total_balance: Optional[float]
    interest_rate: Optional[float]
    minimum_payment: Optional[float]
    total_cumulative: Optional[float]
    remaining_balance: Optional[float]
    remaining_minimum_payment: Optional[float]
    due_date: Optional[datetime]
    open_date: Optional[datetime]
    close_date: Optional[datetime]
    effective_due_date: Optional[datetime]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.paid = round(float(self.raw["paid"]), 2)
        self.interest = round(float(self.raw["interest"]), 2)
        self.past_balance = round(float(self.raw["past_balance"]), 2)
        self.total_balance = round(float(self.raw["total_balance"]), 2)
        self.interest_rate = round(float(self.raw["interest_rate"]), 2)
        self.minimum_payment = round(float(self.raw["minimum_payment"]), 2)
        self.total_cumulative = round(float(self.raw["total_cumulative"]), 2)

        if self.raw.get("remaining_balance"):
            self.remaining_balance = round(float(self.raw["remaining_balance"]), 2)

        if self.raw.get("remaining_minimum_payment"):
            self.remaining_minimum_payment = round(float(self.raw["remaining_minimum_payment"]), 2)

        due_date = self.raw["due_date"]
        self.due_date = datetime.strptime(due_date, "%Y-%m-%d").replace(tzinfo=timezone)

        open_date = self.raw["open_date"]
        self.open_date = datetime.strptime(open_date, "%Y-%m-%d").replace(tzinfo=timezone)

        close_date = self.raw["close_date"]
        self.close_date = datetime.strptime(close_date, "%Y-%m-%d").replace(tzinfo=timezone)

        effective_due_date = self.raw["effective_due_date"]
        self.effective_due_date = datetime.strptime(effective_due_date, "%Y-%m-%d").replace(tzinfo=timezone)


class AccountEvent(BaseModel):
    raw: dict
    typename: Optional[str]
    title: Optional[str]
    detail: Optional[str]
    date_tz: Optional[datetime]
    amount: Optional[float]
    origin_account: Optional[dict]
    destination_account: Optional[dict]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        del self.raw["id"]
        self.typename = self.raw["__typename"]
        self.title = self.raw["title"]
        self.detail = self.raw["detail"]

        postDate = self.raw["postDate"]
        self.date_tz = datetime.strptime(postDate, "%Y-%m-%d").replace(tzinfo=timezone)

        self.amount = round(float(self.raw["amount"]), 2)

        if self.raw.get("originAccount"):
            self.origin_account = self.raw["originAccount"]

        if self.raw.get("destinationAccount"):
            self.destination_account = self.raw["destinationAccount"]


class BillDetails(BaseModel):
    raw: dict
    state: Optional[str]
    due_date: Optional[datetime]
    open_date: Optional[datetime]
    close_date: Optional[datetime]
    effective_due_date: Optional[datetime]
    late_interest_rate: Optional[float]
    past_balance: Optional[float]
    late_fee: Optional[float]
    total_balance: Optional[float]
    interest_rate: Optional[float]
    total_cumulative: Optional[float]
    paid: Optional[float]
    interest: Optional[float]
    minimum_payment: Optional[float]
    line_items: Optional[list]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.state = self.raw.get("state")

        summary = self.raw.get("summary")
        due_date = summary["due_date"]
        self.due_date = datetime.strptime(due_date, "%Y-%m-%d").replace(tzinfo=timezone)

        open_date = summary["open_date"]
        self.open_date = datetime.strptime(open_date, "%Y-%m-%d").replace(tzinfo=timezone)

        close_date = summary["close_date"]
        self.close_date = datetime.strptime(close_date, "%Y-%m-%d").replace(tzinfo=timezone)

        effective_due_date = summary["effective_due_date"]
        self.effective_due_date = datetime.strptime(effective_due_date, "%Y-%m-%d").replace(tzinfo=timezone)

        self.late_interest_rate = round(float(summary["late_interest_rate"]), 2)
        self.past_balance = round(float(summary["past_balance"]), 2)
        self.late_fee = round(float(summary["late_fee"]), 2)
        self.total_balance = round(float(summary["total_balance"]), 2)
        self.interest_rate = round(float(summary["interest_rate"]), 2)
        self.total_cumulative = round(float(summary["total_cumulative"]), 2)
        self.paid = round(float(summary["paid"]), 2)
        self.interest = round(float(summary["interest"]), 2)
        self.minimum_payment = round(float(summary["minimum_payment"]), 2)

        self.line_items = []
        for item in self.raw.get("line_items", []):
            self.line_items.append({
                "amount": item["amount"],
                "index": item.get("index"),
                "title": item.get("title"),
                "post_date": item.get("post_date"),
                "category": item.get("category"),
                "charges": item.get("charges"),
            })


def process_card_feed(input_files=None):
    card_feed_file = max(get_files(config.export_path, '*/card_feed.json'))
    card_feed_data = json.loads(card_feed_file.read_bytes())
    for event in card_feed_data["events"]:
        yield CardFeedEvent(event)


def process_card_statements(input_files=None):
    card_statements_file = max(get_files(config.export_path, '*/card_statements.json'))
    card_statements_data = json.loads(card_statements_file.read_bytes())
    for event in card_statements_data:
        yield CardFeedEvent(event)


def process_bills(input_files=None):
    bills_file = max(get_files(config.export_path, '*/bills.json'))
    bills_data = json.loads(bills_file.read_bytes())
    for event in bills_data:
        if 'overdue' == event.get("state"):
            yield Bills(event.get("summary"))


def process_account_feed(input_files=None):
    account_feed_file = max(get_files(config.export_path, '*/account_feed.json'))
    account_feed_data = json.loads(account_feed_file.read_bytes())
    for event in account_feed_data:
        yield AccountEvent(event)


def process_account_statements(input_files=None):
    account_statements_file = max(get_files(config.export_path, '*/account_statements.json'))
    account_statements_data = json.loads(account_statements_file.read_bytes())

    for event in account_statements_data:
        yield AccountEvent(event)


def process_bill_details(input_files=None):
    if not input_files:
        bill_detail_files = get_files(config.export_path, '*/*bill-detail.json')

    for bill_file in bill_detail_files:
        bill_data = json.loads(bill_file.read_bytes())
        bill = bill_data["bill"]
        yield BillDetails(bill)
