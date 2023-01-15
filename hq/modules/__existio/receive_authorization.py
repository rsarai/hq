from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
import requests

CLIENT_ID = "<client-id>"
CLIENT_SECRET = "<client-secret>"
REDIRECT_URI = 'http://localhost:8000/'

# create a class to handle our http request
class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        # parse the path of this request into its parts
        parts = urlparse(self.path)
        # then parse the query parameters into a dict
        query = parse_qs(parts.query)
        # and then get the code we need out of the dict
        code = query['code'][0]

        # tell the browser it worked
        self.send_response(200)
        self.wfile.write(b'OK!\n')
        # then get our access token
        self.get_token(code)

    def get_token(self, code):
        # make our request using our new code, and some other client details
        response = requests.post('https://exist.io/oauth2/access_token', {
            'grant_type':'authorization_code',
            'code': code,
            'client_id': CLIENT_ID,
            'client_secret': CLIENT_SECRET,
            'redirect_uri': REDIRECT_URI,
        })
        # parse the response into json
        data = response.json()
        print('Access token: ', data['access_token'])
        print('Refresh token:', data['refresh_token'])


# create a http server and listen for one request only
server_address = ('127.0.0.1', 8000)
httpd = HTTPServer(server_address, Handler)
httpd.handle_request()
httpd.server_close()
