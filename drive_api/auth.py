import os

import requests
from oauth2client import file, client, tools

SCOPES = 'https://www.googleapis.com/auth/drive'
DIR_PATH = os.path.dirname(os.path.realpath(__file__))
REVOKE = "https://accounts.google.com/o/oauth2/revoke"


def drive_login() -> client.Credentials:
    token = os.path.join(DIR_PATH, 'token.json')
    store = file.Storage(token)
    credentials = store.get()
    if not credentials or credentials.invalid:
        client_id = os.path.join(DIR_PATH, 'client_secret.json')
        flow = client.flow_from_clientsecrets(client_id, SCOPES)
        flags = tools.argparser.parse_args(args=[])
        credentials = tools.run_flow(flow, store, flags)

    return credentials


def drive_logout() -> None:
    token = os.path.join(DIR_PATH, 'token.json')
    store = file.Storage(token)
    credentials = store.get()
    if credentials:
        requests.post(url=REVOKE, params={'token': credentials.access_token},
                      headers={'Content-type': 'application/x-www-form-urlencoded'})
    os.remove(token)
