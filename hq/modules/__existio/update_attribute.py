import requests, json

TOKEN = 'write_access_token'

def make_update(attribute, date, value):
    return {'name': attribute, 'date': date, 'value': value}

def update_attributes(token, updates):
    # make the json string to send to Exist
    body = json.dumps(updates)

    # make the POST request, sending the json as the POST body
    # we need a content-type header so Exist knows it's json
    response = requests.post("https://exist.io/api/2/attributes/update/",
        data=body,
        headers={'Authorization':f'Bearer {token}',
                 'Content-type':'application/json'})

    if response.status_code == 200:
        # a 200 status code indicates a successful outcome
        print("Updated successfully.")
    else:
        # print the error if something went wrong
        data = response.json()
        print("Error:", data)

daylio_data = [
    ["2023-01-14", "good", "Shopping | family | movies & tv | medium sleep | delivery | Beer | Coffee | sunny | energy medium | attention medium | time high | Vet | Walk | country"],
]

# for i in daylio_data:
#     for activity in i[2].split(" | "):
#         name = activity.strip()
#         if name == "movies & tv":
#             name = "movie__tv"
#         update = make_update(name.replace(" ", "_"), i[0], True)
#         update_attributes(TOKEN, [update])


MOOD = {
    "rad": 5,
    "good": 4,
    "meh": 3,
    "bad": 2,
    "awful": 1,
}

# mood
for i in daylio_data:
    name = "Daylio_Mood"
    rate = MOOD[i[1]]
    update = make_update(name, i[0], rate)
    update_attributes(TOKEN, [update])
