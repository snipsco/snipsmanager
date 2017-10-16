import sys
import os
import requests
import webbrowser

import socket

class Server:

    def start(self):
        print("Starting HTTP server...")
        HOST, PORT = '', 8000

        listen_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        listen_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        listen_socket.bind((HOST, PORT))
        listen_socket.listen(1)
        print 'Serving HTTP on port %s ...' % PORT
        while True:
            client_connection, client_address = listen_socket.accept()
            request = client_connection.recv(1024)
            print request

            #     http_response = """\
            # HTTP/1.1 200 OK

            # Hello, World!
            # """
            #     client_connection.sendall(http_response)
            client_connection.close()

client_id = "765e1498b29949c5a36dbcae4eea8330"
redirect_url = "http://localhost:8000/snipssonos"
state = "DOLp3ARPu9"
auth_request_uri = "https://accounts.spotify.com/authorize/?client_id={}&response_type=code&redirect_uri={}&scope=user-read-private%20user-read-email&state={}".format(client_id, redirect_url, state)

# r = requests.get(auth_request_uri)

# print("=============")
# print(str(auth_request_uri))

webbrowser.open(auth_request_uri)

s = Server()
s.start()

# os.environ["SPOTIPY_CLIENT_ID"] = "765e1498b29949c5a36dbcae4eea8330"
# os.environ["SPOTIPY_CLIENT_SECRET"] = "72e1fb080f3a49f99b357fd6b8d79cd7"
# os.environ["SPOTIPY_REDIRECT_URI"] = "http://localhost:8000/snipssonos"

# scope = 'user-library-read'
# username = "michaelfester"

# token = util.prompt_for_user_token(username, scope)

# if token:
#     sp = spotipy.Spotify(auth=token)
#     results = sp.current_user_saved_tracks()
#     for item in results['items']:
#         track = item['track']
#         print track['name'] + ' - ' + track['artists'][0]['name']
# else:
#     print "Can't get token for", username