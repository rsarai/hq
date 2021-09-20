import json
import zipfile

from datetime import date, datetime
from typing import Optional
from pydantic import BaseModel

from hq.common import get_files, parse_datetime
from hq.config import GoogleTakeout as config


KEY = "Google Play Store"
EXCLUDE_KEY = 'Minhaatividade.html'

INCLUDE_FILES = [
    'Purchase History.json',
    'Subscriptions.json',
    'Reviews.json',
    'Order History.json',
    'Installs.json',
]


class Order(BaseModel):
    raw: dict
    id: Optional[str]
    date_tz: Optional[datetime]
    price: Optional[str]
    tax: Optional[str]
    refund: Optional[str]
    is_renewal: Optional[bool]
    title: Optional[str]
    description: str = 'Google Play Store: Order'

    def __init__(self, raw):
        data = {"raw": raw}

        order = raw.get("orderHistory", {})
        data["id"] = order.get("id")
        data["is_renewal"] = order.get("renewalOrder")
        data["refund"] = order.get("refundAmount")
        data["price"] = order.get("totalPrice")
        data["tax"] = order.get("tax")

        date = order.get("creationTime")
        data["date_tz"] = parse_datetime(date, '%Y-%m-%dT%H:%M:%S.%fZ')

        data["title"] = ", ".join([i.get('doc', {}).get('title') for i in order.get("lineItem", [])])
        super().__init__(**data)


class Review(BaseModel):
    raw: dict
    title: Optional[str]
    date_tz: Optional[datetime]
    rating: Optional[int]
    comment: Optional[str]
    description: str = 'Google Play Store: Review'

    def __init__(self, raw):
        data = {"raw": raw}

        review = raw.get("review", {})
        data["title"] = review.get("document", {}).get("title")

        date = review.get("creationTime")
        data["date_tz"] = parse_datetime(date, '%Y-%m-%dT%H:%M:%S.%fZ')

        data["rating"] = review.get("starRating")
        data["comment"] = review.get("title") + " " + review.get("comment")
        super().__init__(**data)


class Install(BaseModel):
    raw: dict
    title: Optional[str]
    date_tz: Optional[datetime]
    last_update: Optional[datetime]
    description: str = 'Google Play Store: Install'

    def __init__(self, raw):
        data = {"raw": raw}
        install = raw.get("install", {})

        date = install.get("firstInstallationTime")
        try:
            data["date_tz"] = parse_datetime(date, '%Y-%m-%dT%H:%M:%S.%fZ')
        except:
            data["date_tz"] = parse_datetime(date, '%Y-%m-%dT%H:%M:%SZ')
        date = install.get("lastUpdateTime")

        try:
            data["last_update"] = parse_datetime(date, '%Y-%m-%dT%H:%M:%S.%fZ')
        except ValueError:
            data["last_update"] = parse_datetime(date, '%Y-%m-%dT%H:%M:%SZ')

        data["title"] = install.get("doc", {}).get("title")
        super().__init__(**data)


class Purchase(BaseModel):
    raw: dict
    invoice_price: Optional[str]
    title: Optional[str]
    date_tz: Optional[datetime]
    description: str = 'Google Play Store: Purchase'

    def __init__(self, raw):
        data = {"raw": raw}
        data["invoice_price"] = raw.get("purchaseHistory", {}).get("invoicePrice").replace("\xa0", " ")
        data["title"] = raw.get("purchaseHistory", {}).get("doc", {}).get("title")

        date = raw.get("purchaseHistory", {}).get("purchaseTime")
        data["date_tz"] = parse_datetime(date, '%Y-%m-%dT%H:%M:%S.%fZ')
        super().__init__(**data)


class Subscription(BaseModel):
    raw: dict
    period: Optional[str]
    title: Optional[str]
    pricing: Optional[list]
    action_record: Optional[dict]
    state: Optional[str]
    expiration_date: Optional[datetime]
    description: str = 'Google Play Store: Subscription'


    def __init__(self, raw):
        data = {"raw": raw}

        period_info = raw.get("subscription", {}).get("period")
        data["period"] = f"{period_info['count']} {period_info['unit']}"
        data["title"] = raw.get("subscription", {}).get("doc", {}).get("title")

        date = raw.get("subscription", {}).get("expirationDate")
        if date:
            data["expiration_date"] = parse_datetime(date, '%Y-%m-%dT%H:%M:%S.%fZ')

        data["pricing"] = raw.get("subscription", {}).get("pricing")
        data["action_record"] = raw.get("subscription", {}).get("userChangeRecord")
        data["state"] = raw.get("subscription", {}).get("state")
        super().__init__(**data)


def get_file_paths():
    return [
        max(get_files(config.export_path, "takeout*")),
        max(get_files(config.export_path, "vinta*")),
        max(get_files(config.export_path, "ecomp*")),
    ]


def process(input_files=None):
    CLASSES_FILES = [Purchase, Subscription, Review, Order, Install]
    if not input_files:
        input_files = get_file_paths()

    # for each account file export
    for zip_path in input_files:
        zf = zipfile.ZipFile(zip_path)

        # for each one of the pre-selected info files
        for include_key, pydantic_class in zip(INCLUDE_FILES, CLASSES_FILES):
            play_store_files = [i for i in zf.filelist if KEY in str(i) and include_key in str(i)]

            # for each one of the found files
            for file_name in play_store_files:
                with zf.open(file_name) as f:
                    content = json.load(f)

                    # for each item saved on the file
                    for item in content:
                        yield pydantic_class(item)
