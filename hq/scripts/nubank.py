from hq.modules import nubank
from dateutil import tz
to_zone = tz.gettz('America/Recife')


feed = list(nubank.process_bill_details())

for f in feed:
    if f.due_date.strftime('%m/%Y') == "06/2022":
        print(f"===================== {f.due_date.strftime('%m/%Y')}")
        for i in f.line_items:
            amount = str(i["amount"]).replace(".", ",")
            t = i["title"]
            pd = i["post_date"]
            print(f"{t}; {amount}; {pd}")


feed = list(nubank.process_future_bill_details())
for f in feed:
    print(f"===================== {f.due_date.strftime('%m/%Y')}")
    for i in f.line_items:
        amount = str(i["amount"]).replace(".", ",")
        t = i["title"]
        pd = i["post_date"]
        print(f"{t}; {amount}; {pd}")
