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

        description = raw.get("description")
        category = raw["category"]
        title = raw["title"]
        data = {
            "raw": raw,
            "description": description,
            "category": category,
            "title": title,
        }

        time = raw["time"]
        if '.' in time:
            date_tz = datetime.strptime(time, "%Y-%m-%dT%H:%M:%S.%fZ").replace(tzinfo=timezone)
        else:
            date_tz = datetime.strptime(time, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone)
        data["date_tz"] = date_tz

        if raw.get("amount"):
            amount = round(float(raw["amount"]), 2)
            data["amount"] = amount

        if raw.get("amount_without_iof"):
            amount_without_iof = round(float(raw["amount_without_iof"]), 2)
            data["amount_without_iof"] = amount_without_iof

        super().__init__(**data)


class Bills(BaseModel):
    raw: dict
    paid: Optional[float]
    interest: Optional[float]
    past_balance: Optional[float]
    total_balance: Optional[float]
    interest_rate: Optional[float]
    total_cumulative: Optional[float]
    remaining_balance: Optional[float]
    remaining_minimum_payment: Optional[float]
    minimum_payment: Optional[float]
    due_date: Optional[datetime]
    open_date: Optional[datetime]
    close_date: Optional[datetime]
    effective_due_date: Optional[datetime]

    def __init__(self, raw):
        data = {"raw": raw}
        paid = round(float(raw["paid"]), 2)
        interest = round(float(raw["interest"]), 2)
        past_balance = round(float(raw["past_balance"]), 2)
        total_balance = round(float(raw["total_balance"]), 2)
        interest_rate = round(float(raw["interest_rate"]), 2)
        minimum_payment = round(float(raw["minimum_payment"]), 2)
        total_cumulative = round(float(raw["total_cumulative"]), 2)
        data["paid"] = paid
        data["interest"] = interest
        data["past_balance"] = past_balance
        data["total_balance"] = total_balance
        data["interest_rate"] = interest_rate
        data["minimum_payment"] = minimum_payment
        data["total_cumulative"] = total_cumulative

        if raw.get("remaining_balance"):
            remaining_balance = round(float(raw["remaining_balance"]), 2)
            data["remaining_balance"] = remaining_balance

        if raw.get("remaining_minimum_payment"):
            remaining_minimum_payment = round(float(raw["remaining_minimum_payment"]), 2)
            data["remaining_minimum_payment"] = remaining_minimum_payment

        due_date = raw["due_date"]
        due_date = datetime.strptime(due_date, "%Y-%m-%d").replace(tzinfo=timezone)

        open_date = raw["open_date"]
        open_date = datetime.strptime(open_date, "%Y-%m-%d").replace(tzinfo=timezone)

        close_date = raw["close_date"]
        close_date = datetime.strptime(close_date, "%Y-%m-%d").replace(tzinfo=timezone)

        effective_due_date = raw["effective_due_date"]
        effective_due_date = datetime.strptime(effective_due_date, "%Y-%m-%d").replace(tzinfo=timezone)

        data["due_date"] = due_date
        data["open_date"] = open_date
        data["close_date"] = close_date
        data["effective_due_date"] = effective_due_date
        super().__init__(**data)


class AccountEvent(BaseModel):
    raw: dict
    typename: Optional[str]
    title: Optional[str]
    detail: Optional[str]
    date_tz: Optional[datetime]
    amount: Optional[float]
    origin_account: Optional[dict]
    destination_account: Optional[dict]

    def __init__(self, raw):
        del raw["id"]
        data = {"raw": raw}

        data["typename"] = raw["__typename"]
        data["title"]  = raw["title"]
        data["detail"] = raw["detail"]

        postDate = raw["postDate"]
        data["date_tz"] = datetime.strptime(postDate, "%Y-%m-%d").replace(tzinfo=timezone)

        if raw.get("amount"):
            data["amount"] = round(float(raw["amount"]), 2)

        if raw.get("originAccount"):
            origin_account = raw["originAccount"]
            data["origin_account"] = origin_account

        if raw.get("destinationAccount"):
            destination_account = raw["destinationAccount"]
            data["destination_account"] = destination_account

        super().__init__(**data)


class BillDetails(BaseModel):
    raw: dict
    state: Optional[str]
    late_interest_rate: Optional[float]
    past_balance: Optional[float]
    late_fee: Optional[float]
    total_balance: Optional[float]
    interest_rate: Optional[float]
    total_cumulative: Optional[float]
    interest: Optional[float]
    line_items: Optional[list]
    paid: Optional[float]
    minimum_payment: Optional[float]
    due_date: Optional[datetime]
    open_date: Optional[datetime]
    close_date: Optional[datetime]
    effective_due_date: Optional[datetime]

    def __init__(self, raw):
        del raw["id"]
        del raw["_links"]
        data = {"raw": raw}
        data["state"] = raw.get("state")

        summary = raw.get("summary")
        due_date = summary["due_date"]
        data["due_date"] = datetime.strptime(due_date, "%Y-%m-%d").replace(tzinfo=timezone)

        open_date = summary["open_date"]
        data["open_date"] = datetime.strptime(open_date, "%Y-%m-%d").replace(tzinfo=timezone)

        close_date = summary["close_date"]
        data["close_date"] = datetime.strptime(close_date, "%Y-%m-%d").replace(tzinfo=timezone)

        effective_due_date = summary["effective_due_date"]
        data["effective_due_date"] = datetime.strptime(effective_due_date, "%Y-%m-%d").replace(tzinfo=timezone)

        data["late_interest_rate"] = round(float(summary["late_interest_rate"]), 2)
        data["past_balance"] = round(float(summary["past_balance"]), 2)
        data["late_fee"] = round(float(summary["late_fee"]), 2)
        data["total_balance"] = round(float(summary["total_balance"]), 2)
        data["interest_rate"] = round(float(summary["interest_rate"]), 2)
        data["total_cumulative"] = round(float(summary["total_cumulative"]), 2)
        data["paid"] = round(float(summary["paid"]), 2)
        data["interest"] = round(float(summary["interest"]), 2)
        data["minimum_payment"] = round(float(summary["minimum_payment"]), 2)

        line_items = []
        for item in raw.get("line_items", []):
            line_items.append({
                "amount": item["amount"],
                "index": item.get("index"),
                "title": item.get("title"),
                "post_date": item.get("post_date"),
                "category": item.get("category"),
                "charges": item.get("charges"),
            })
        data["line_items"] = line_items

        super().__init__(**data)


def get_card_feed_files():
    return max(get_files(config.export_path, '*/card_feed.json'))


def get_card_statements_files():
    return max(get_files(config.export_path, '*/card_statements.json'))


def get_bills_files():
    return max(get_files(config.export_path, '*/bills.json'))


def get_account_feed_files():
    return max(get_files(config.export_path, '*/account_feed.json'))


def get_account_statements_files():
    return max(get_files(config.export_path, '*/account_statements.json'))


def get_bill_details_files():
    return get_files(config.export_path, '*/*bill-detail.json')


def get_file_paths():
    return {
        "card_feed": get_card_feed_files(),
        "account_feed": get_account_feed_files(),
        "bill_detail": get_bill_details_files(),
    }


def process_card_feed(input_files=None):
    if not input_files:
        input_files = get_card_feed_files()

    card_feed_data = json.loads(input_files.read_bytes())
    for event in card_feed_data["events"]:
        yield CardFeedEvent(event)


def process_card_statements(input_files=None):
    """
        Appears (not sure) to be a simplified version of card_feed
    """
    if not input_files:
        input_files = get_card_statements_files()

    card_statements_data = json.loads(input_files.read_bytes())
    for event in card_statements_data:
        yield CardFeedEvent(event)


def process_bills(input_files=None):
    """
        Simplified version of the bill_details
    """
    if not input_files:
        input_files = get_bills_files()

    bills_data = json.loads(input_files.read_bytes())
    for event in bills_data:
        if 'overdue' == event.get("state"):
            yield Bills(event.get("summary"))


def process_account_feed(input_files=None):
    if not input_files:
        input_files = get_account_feed_files()

    account_feed_data = json.loads(input_files.read_bytes())
    for event in account_feed_data:
        yield AccountEvent(event)


def process_account_statements(input_files=None):
    """
        Simplified version of account_feed
    """
    if not input_files:
        input_files = get_account_statements_files()

    account_statements_data = json.loads(input_files.read_bytes())

    for event in account_statements_data:
        yield AccountEvent(event)


def process_bill_details(input_files=None):
    if not input_files:
        input_files = get_bill_details_files()

    for bill_file in input_files:
        bill_data = json.loads(bill_file.read_bytes())
        bill = bill_data["bill"]
        yield BillDetails(bill)
