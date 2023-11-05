from hq.modules import nubank
from dateutil import tz
to_zone = tz.gettz('America/Recife')


feed = list(nubank.process_future_bill_details())

for f in feed:
    if f.due_date.strftime('%m/%Y') == "08/2022":
        print(f"===================== {f.due_date.strftime('%m/%Y')}")
        for i in f.line_items:
            amount = str(i["amount"]).replace(".", ",")
            t = i["title"]
            pd = i["post_date"]
            print(f"{t}; {amount}; {pd};")

# from hq.modules import nubank
# from dateutil import tz

# to_zone = tz.gettz('America/Recife')
# feed = list(nubank.process_future_bill_details())
# for f in feed:
#     print(f"===================== {f.due_date.strftime('%m/%Y')}, {len(f.line_items)}")
#     for i in f.line_items:
#         amount = str(i["amount"]).replace(".", ",")
#         t = i["title"]
#         pd = i["post_date"]
#         print(f"{t}; {amount}; {pd}")

for f in feed:
    print(f.typename, f.title, f.detail, f.amount, f.raw["postDate"])
