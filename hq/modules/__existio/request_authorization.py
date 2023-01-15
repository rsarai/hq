from urllib.parse import urlencode

CLIENT_ID = "<client-id>"
URL = 'https://exist.io/oauth2/authorize'
REDIRECT_URI = 'http://localhost:8000/'

# the parameters we'll be sending
params = {'client_id': CLIENT_ID,
          'response_type':'code',
          'redirect_uri':REDIRECT_URI,
          'scope':'media_write',
         }

# let's encode them appropriately for a URL
querystring = urlencode(params)
# and finally print the complete result to the terminal
print(f"{URL}?{querystring}")
