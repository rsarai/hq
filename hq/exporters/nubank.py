"""
The following code generates the certificate necessary
> pynubank

Copy the cert file to a safe place
After that you can run the following script
https://github.com/andreroggeri/pynubank/blob/master/examples/login-certificate.md
"""
import json
import sys
import pytz
from pathlib import Path
from datetime import datetime

from pynubank import Nubank
from pynubank.utils.http import HttpClient

sys.path.append('/home/sarai/github-projects/hq')
from hq.config import Nubank as config


def dumper(data, path, filename):
    path.mkdir(parents=True, exist_ok=True)
    js = json.dumps(data, ensure_ascii=False, indent=1)
    f = path / filename
    f.write_text(js)


def generate_export():
    nu = Nubank()
    nu.authenticate_with_cert(
        config.authentication["cpf"],
        config.authentication["password"],
        config.authentication["cert_path"]
    )
    folder_name = datetime.today().strftime('%Y_%m_%d')
    export_path = config.export_path

    card_feed = nu.get_card_feed()
    dumper(card_feed, Path(export_path + "/" + folder_name), "card_feed.json")

    res = nu.get_card_statements()
    dumper(res, Path(export_path + "/" + folder_name), "card_statements.json")

    res = nu.get_bills()
    dumper(res, Path(export_path + "/" + folder_name), "bills.json")

    for bill in res:
        if bill["_links"] == {}:
            continue

        due_date = bill["summary"]["due_date"]
        bill_detail = nu.get_bill_details(bill)

        dumper(bill_detail, Path(export_path + "/" + folder_name), f"{due_date}-bill-detail.json")
        # only getting the last one
        break

    res = nu.get_account_feed()
    dumper(res, Path(export_path + "/" + folder_name), "account_feed.json")

    res = nu.get_account_statements()
    dumper(res, Path(export_path + "/" + folder_name), "account_statements.json")

    res = nu.get_account_balance()
    dumper(res, Path(export_path + "/" + folder_name), "account_balance.json")

    res = nu.get_account_investments_details()
    dumper(res, Path(export_path + "/" + folder_name), "account_investments_details.json")



generate_export()
