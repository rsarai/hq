import json
from typing import Optional

from datetime import datetime
from pydantic import BaseModel

from hq.common import get_files, parse_datetime
from hq.config import Nubank as config


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
            date_tz = parse_datetime(time, "%Y-%m-%dT%H:%M:%S.%fZ")
        else:
            date_tz = parse_datetime(time, "%Y-%m-%dT%H:%M:%SZ")
        data["date_tz"] = date_tz

        if raw.get("amount"):
            amount = str(raw["amount"])
            data["amount"] = float(amount[:-2] + '.' + amount[-2:])

        if raw.get("amount_without_iof"):
            amount_without_iof = str(raw["amount_without_iof"])
            data["amount_without_iof"] = float(amount_without_iof[:-2] + '.' + amount_without_iof[-2:])

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

        paid = str(raw["paid"])
        interest = round(float(raw["interest"]), 2)
        past_balance = round(float(raw["past_balance"]), 2)
        total_balance = round(float(raw["total_balance"]), 2)
        interest_rate = round(float(raw["interest_rate"]), 2)
        minimum_payment = round(float(raw["minimum_payment"]), 2)
        total_cumulative = round(float(raw["total_cumulative"]), 2)
        data["paid"] = float(paid[:-2] + '.' + paid[-2:])
        data["interest"] = interest
        data["past_balance"] = past_balance
        data["total_balance"] = total_balance
        data["interest_rate"] = interest_rate
        data["minimum_payment"] = minimum_payment
        data["total_cumulative"] = total_cumulative

        if raw.get("remaining_balance"):
            remaining_balance = str(raw["remaining_balance"])
            data["remaining_balance"] = float(remaining_balance[:-2] + '.' + remaining_balance[-2:])

        if raw.get("remaining_minimum_payment"):
            remaining_minimum_payment = str(raw["remaining_minimum_payment"])
            data["remaining_minimum_payment"] = float(remaining_minimum_payment[:-2] + '.' + remaining_minimum_payment[-2:])

        due_date = raw["due_date"]
        due_date = parse_datetime(due_date, "%Y-%m-%d")

        open_date = raw["open_date"]
        open_date = parse_datetime(open_date, "%Y-%m-%d")

        close_date = raw["close_date"]
        close_date = parse_datetime(close_date, "%Y-%m-%d")

        effective_due_date = raw["effective_due_date"]
        effective_due_date = parse_datetime(effective_due_date, "%Y-%m-%d")

        data["due_date"] = due_date
        data["datetime"] = close_date
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
        data["date_tz"] = parse_datetime(postDate, "%Y-%m-%d")

        if raw.get("amount"):
            amount = str(raw["amount"])
            amount = amount if '.' not in amount else amount.replace('.', '0')
            data["amount"] = float(amount[:-2] + '.' + amount[-2:])

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
        if raw.get('id'):
            del raw["id"]

        if raw.get('_links'):
            del raw["_links"]
        data = {"raw": raw}
        data["state"] = raw.get("state")

        summary = raw.get("summary")
        due_date = summary["due_date"]
        data["due_date"] = parse_datetime(due_date, "%Y-%m-%d")

        open_date = summary["open_date"]
        data["open_date"] = parse_datetime(open_date, "%Y-%m-%d")

        close_date = summary["close_date"]
        data["close_date"] = parse_datetime(close_date, "%Y-%m-%d")

        effective_due_date = summary["effective_due_date"]
        data["effective_due_date"] = parse_datetime(effective_due_date, "%Y-%m-%d")

        data["late_interest_rate"] = round(float(summary["late_interest_rate"]), 2)
        data["past_balance"] = round(float(summary["past_balance"]), 2)
        data["late_fee"] = round(float(summary["late_fee"]), 2)
        data["interest_rate"] = round(float(summary["interest_rate"]), 2)

        total_balance = str(summary["total_balance"])
        data["total_balance"] = float(total_balance[:-2] + '.' + total_balance[-2:])

        total_cumulative = str(summary["total_cumulative"])
        data["total_cumulative"] = float(total_cumulative[:-2] + '.' + total_cumulative[-2:])

        if summary["paid"] > 0:
            paid = str(summary["paid"])
            data["paid"] = float(paid[:-2] + '.' + paid[-2:])
        else:
            data["paid"] = summary["paid"]

        if summary["minimum_payment"] > 0:
            minimum_payment = str(summary["minimum_payment"])
            data["minimum_payment"] = float(minimum_payment[:-2] + '.' + minimum_payment[-2:])
        else:
            data["minimum_payment"] = summary["minimum_payment"]

        data["interest"] = round(float(summary["interest"]), 2)

        line_items = []
        for item in raw.get("line_items", []):
            amount = str(item["amount"])
            line_items.append({
                "amount": float(amount[:-2] + '.' + amount[-2:]),
                "index": item.get("index"),
                "title": item.get("title"),
                "post_date": item.get("post_date"),
                "category": item.get("category"),
                "charges": item.get("charges"),
            })
        data["line_items"] = line_items

        super().__init__(**data)


def get_card_feed_files():
    return [max(get_files(config.export_path, '*/card_feed.json'))]


def get_card_statements_files():
    return [max(get_files(config.export_path, '*/card_statements.json'))]


def get_bills_files():
    return [max(get_files(config.export_path, '*/bills.json'))]


def get_account_feed_files():
    return [max(get_files(config.export_path, '*/account_feed.json'))]


def get_account_statements_files():
    return [max(get_files(config.export_path, '*/account_statements.json'))]


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

    for card_feed_file in input_files:
        card_feed_data = json.loads(card_feed_file.read_bytes())
        for event in card_feed_data["events"]:
            yield CardFeedEvent(event)


def process_card_statements(input_files=None):
    """
        Appears (not sure) to be a simplified version of card_feed
    """
    if not input_files:
        input_files = get_card_statements_files()

    for card_statements_file in input_files:
        card_statements_data = json.loads(card_statements_file.read_bytes())
        for event in card_statements_data:
            yield CardFeedEvent(event)


def process_bills(input_files=None):
    """
        Simplified version of the bill_details
    """
    if not input_files:
        input_files = get_bills_files()

    for bills_file in input_files:
        bills_data = json.loads(bills_file.read_bytes())
        for event in bills_data:
            if 'overdue' == event.get("state"):
                yield Bills(event.get("summary"))


def process_account_feed(input_files=None):
    if not input_files:
        input_files = get_account_feed_files()

    for account_file in input_files:
        account_feed_data = json.loads(account_file.read_bytes())
        for event in account_feed_data:
            yield AccountEvent(event)


def process_account_statements(input_files=None):
    """
        Simplified version of account_feed
    """
    if not input_files:
        input_files = get_account_statements_files()

    for account_stat_file in input_files:
        account_statements_data = json.loads(account_stat_file.read_bytes())
        for event in account_statements_data:
            yield AccountEvent(event)


def process_bill_details(input_files=None):
    if not input_files:
        input_files = get_bill_details_files()

    for bill_file in input_files:
        bill_data = json.loads(bill_file.read_bytes())
        bill = bill_data["bill"]
        yield BillDetails(bill)
