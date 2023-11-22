from enum import IntEnum
from pprint import PrettyPrinter
import requests, json

TOKEN = 'write_access_token'

# let's make some constants to represent Exist's value types
class ValueType(IntEnum):
    QUANTITY = 0
    DECIMAL = 1
    STRING = 2
    DURATION = 3
    TIMEOFDAY = 4
    PERCENTAGE = 5
    BOOLEAN = 7
    SCALE = 8

def create_attribute(token, label, value_type, group, manual):
    # make the json string to send to Exist
    body = json.dumps([
        {'label': label,
         'value_type': value_type,
         'group': group,
         'manual': manual
        }])

    # make the POST request, sending the json as the POST body
    # we need a content-type header so Exist knows it's json
    response = requests.post("https://exist.io/api/2/attributes/create/",
        data=body,
        headers={'Authorization':f'Bearer {token}',
                 'Content-type':'application/json'})

    if response.status_code == 200:
        # a 200 status code indicates a successful outcome
        # let's get out the full version of our attribute
        data = response.json()
        obj = data['success'][0]
        print("Created successfully:")
        # and let's print it (nicely) so we can see its fields
        pp = PrettyPrinter()
        pp.pprint(obj)
    else:
        # print the error if something went wrong
        data = response.json()
        print("Error:", data)

# call the function with the attribute details we're after

create_attribute(TOKEN, label="Daylio Mood", value_type=ValueType.SCALE, group="mood", manual=False)

create_attribute(TOKEN, label="Family", value_type=ValueType.BOOLEAN, group="custom", manual=False)
create_attribute(TOKEN, label="Friends", value_type=ValueType.BOOLEAN, group="custom", manual=False)
create_attribute(TOKEN, label="Date", value_type=ValueType.BOOLEAN, group="custom", manual=False)
create_attribute(TOKEN, label="Party", value_type=ValueType.BOOLEAN, group="custom", manual=False)
create_attribute(TOKEN, label="Budget", value_type=ValueType.BOOLEAN, group="custom", manual=False)
create_attribute(TOKEN, label="Sad News", value_type=ValueType.BOOLEAN, group="custom", manual=False)
create_attribute(TOKEN, label="Alone Time", value_type=ValueType.BOOLEAN, group="custom", manual=False)

create_attribute(TOKEN, label="Movie & TV", value_type=ValueType.BOOLEAN, group="custom", manual=False)
create_attribute(TOKEN, label="Gaming", value_type=ValueType.BOOLEAN, group="custom", manual=False)
create_attribute(TOKEN, label="Relax", value_type=ValueType.BOOLEAN, group="custom", manual=False)
create_attribute(TOKEN, label="Reading", value_type=ValueType.BOOLEAN, group="custom", manual=False)
create_attribute(TOKEN, label="Writing", value_type=ValueType.BOOLEAN, group="custom", manual=False)
create_attribute(TOKEN, label="Piano", value_type=ValueType.BOOLEAN, group="custom", manual=False)
create_attribute(TOKEN, label="Footbal", value_type=ValueType.BOOLEAN, group="custom", manual=False)
create_attribute(TOKEN, label="Coding", value_type=ValueType.BOOLEAN, group="custom", manual=False)
create_attribute(TOKEN, label="Basketball", value_type=ValueType.BOOLEAN, group="custom", manual=False)
create_attribute(TOKEN, label="Guitar", value_type=ValueType.BOOLEAN, group="custom", manual=False)

create_attribute(TOKEN, label="Sleep Early", value_type=ValueType.BOOLEAN, group="custom", manual=False)
create_attribute(TOKEN, label="Medium Sleep", value_type=ValueType.BOOLEAN, group="custom", manual=False)
create_attribute(TOKEN, label="Bad Sleep", value_type=ValueType.BOOLEAN, group="custom", manual=False)
create_attribute(TOKEN, label="Good Sleep", value_type=ValueType.BOOLEAN, group="custom", manual=False)
create_attribute(TOKEN, label="Tired before 5", value_type=ValueType.BOOLEAN, group="custom", manual=False)
create_attribute(TOKEN, label="Nap", value_type=ValueType.BOOLEAN, group="custom", manual=False)

create_attribute(TOKEN, label="Eat Healthy", value_type=ValueType.BOOLEAN, group="custom", manual=False)
create_attribute(TOKEN, label="Homemade", value_type=ValueType.BOOLEAN, group="custom", manual=False)
create_attribute(TOKEN, label="Restaurant", value_type=ValueType.BOOLEAN, group="custom", manual=False)
create_attribute(TOKEN, label="Delivery", value_type=ValueType.BOOLEAN, group="custom", manual=False)
create_attribute(TOKEN, label="Soda", value_type=ValueType.BOOLEAN, group="custom", manual=False)
create_attribute(TOKEN, label="Beer", value_type=ValueType.BOOLEAN, group="custom", manual=False)
create_attribute(TOKEN, label="Coffee", value_type=ValueType.BOOLEAN, group="custom", manual=False)
create_attribute(TOKEN, label="Pizza", value_type=ValueType.BOOLEAN, group="custom", manual=False)
create_attribute(TOKEN, label="Sweets", value_type=ValueType.BOOLEAN, group="custom", manual=False)
create_attribute(TOKEN, label="Barbecue", value_type=ValueType.BOOLEAN, group="custom", manual=False)
create_attribute(TOKEN, label="Wine", value_type=ValueType.BOOLEAN, group="custom", manual=False)
create_attribute(TOKEN, label="Cooking", value_type=ValueType.BOOLEAN, group="custom", manual=False)

create_attribute(TOKEN, label="Start Early", value_type=ValueType.BOOLEAN, group="custom", manual=False)
create_attribute(TOKEN, label="Focus", value_type=ValueType.BOOLEAN, group="custom", manual=False)
create_attribute(TOKEN, label="Distracted", value_type=ValueType.BOOLEAN, group="custom", manual=False)

create_attribute(TOKEN, label="Sunny", value_type=ValueType.BOOLEAN, group="custom", manual=False)
create_attribute(TOKEN, label="Clouds", value_type=ValueType.BOOLEAN, group="custom", manual=False)
create_attribute(TOKEN, label="Rain", value_type=ValueType.BOOLEAN, group="custom", manual=False)
create_attribute(TOKEN, label="Snow", value_type=ValueType.BOOLEAN, group="custom", manual=False)
create_attribute(TOKEN, label="Heat", value_type=ValueType.BOOLEAN, group="custom", manual=False)
create_attribute(TOKEN, label="Storm", value_type=ValueType.BOOLEAN, group="custom", manual=False)
create_attribute(TOKEN, label="Wind", value_type=ValueType.BOOLEAN, group="custom", manual=False)

create_attribute(TOKEN, label="Solved Hard Puzzle", value_type=ValueType.BOOLEAN, group="custom", manual=False)
create_attribute(TOKEN, label="Work", value_type=ValueType.BOOLEAN, group="custom", manual=False)
create_attribute(TOKEN, label="Work Stress", value_type=ValueType.BOOLEAN, group="custom", manual=False)
create_attribute(TOKEN, label="Slow", value_type=ValueType.BOOLEAN, group="custom", manual=False)
create_attribute(TOKEN, label="Long Meetings", value_type=ValueType.BOOLEAN, group="custom", manual=False)

create_attribute(TOKEN, label="Mental Confusion", value_type=ValueType.BOOLEAN, group="custom", manual=False)
create_attribute(TOKEN, label="Self Reflection", value_type=ValueType.BOOLEAN, group="custom", manual=False)
create_attribute(TOKEN, label="Spiritual", value_type=ValueType.BOOLEAN, group="custom", manual=False)
create_attribute(TOKEN, label="Struggled with Anxiety", value_type=ValueType.BOOLEAN, group="custom", manual=False)
create_attribute(TOKEN, label="Daydreaming", value_type=ValueType.BOOLEAN, group="custom", manual=False)

create_attribute(TOKEN, label="Exercise", value_type=ValueType.BOOLEAN, group="custom", manual=False)
create_attribute(TOKEN, label="Walk", value_type=ValueType.BOOLEAN, group="custom", manual=False)
create_attribute(TOKEN, label="Running", value_type=ValueType.BOOLEAN, group="custom", manual=False)
create_attribute(TOKEN, label="Headache", value_type=ValueType.BOOLEAN, group="custom", manual=False)
create_attribute(TOKEN, label="Shoulder Pain", value_type=ValueType.BOOLEAN, group="custom", manual=False)
create_attribute(TOKEN, label="Sick", value_type=ValueType.BOOLEAN, group="custom", manual=False)
create_attribute(TOKEN, label="Period", value_type=ValueType.BOOLEAN, group="custom", manual=False)
create_attribute(TOKEN, label="Knee Pain ", value_type=ValueType.BOOLEAN, group="custom", manual=False)
create_attribute(TOKEN, label="Medicine", value_type=ValueType.BOOLEAN, group="custom", manual=False)

create_attribute(TOKEN, label="Energy High", value_type=ValueType.BOOLEAN, group="custom", manual=False)
create_attribute(TOKEN, label="Energy Low", value_type=ValueType.BOOLEAN, group="custom", manual=False)
create_attribute(TOKEN, label="Energy Medium", value_type=ValueType.BOOLEAN, group="custom", manual=False)
create_attribute(TOKEN, label="Attention High", value_type=ValueType.BOOLEAN, group="custom", manual=False)
create_attribute(TOKEN, label="Attention Low", value_type=ValueType.BOOLEAN, group="custom", manual=False)
create_attribute(TOKEN, label="Attention Medium", value_type=ValueType.BOOLEAN, group="custom", manual=False)
create_attribute(TOKEN, label="Time High", value_type=ValueType.BOOLEAN, group="custom", manual=False)
create_attribute(TOKEN, label="Time Low", value_type=ValueType.BOOLEAN, group="custom", manual=False)
create_attribute(TOKEN, label="Time Medium", value_type=ValueType.BOOLEAN, group="custom", manual=False)

create_attribute(TOKEN, label="Vet", value_type=ValueType.BOOLEAN, group="custom", manual=False)
create_attribute(TOKEN, label="Dog Walk", value_type=ValueType.BOOLEAN, group="custom", manual=False)
create_attribute(TOKEN, label="Dog Bites", value_type=ValueType.BOOLEAN, group="custom", manual=False)
create_attribute(TOKEN, label="Dog Training", value_type=ValueType.BOOLEAN, group="custom", manual=False)

create_attribute(TOKEN, label="Home", value_type=ValueType.BOOLEAN, group="custom", manual=False)
create_attribute(TOKEN, label="Travel", value_type=ValueType.BOOLEAN, group="custom", manual=False)
create_attribute(TOKEN, label="Outside the usual", value_type=ValueType.BOOLEAN, group="custom", manual=False)
create_attribute(TOKEN, label="Restaurant", value_type=ValueType.BOOLEAN, group="custom", manual=False)
create_attribute(TOKEN, label="Country", value_type=ValueType.BOOLEAN, group="custom", manual=False)

create_attribute(TOKEN, label="Shopping", value_type=ValueType.BOOLEAN, group="custom", manual=False)
