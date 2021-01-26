import os

import requests
from pydrive2.auth import GoogleAuth

DIR_PATH = os.path.dirname(os.path.realpath(__file__))
REVOKE = "https://accounts.google.com/o/oauth2/revoke"


def drive_login() -> GoogleAuth:
    gauth = GoogleAuth()
    gauth.LoadCredentials()
    if gauth.access_token_expired:
        gauth.LocalWebserverAuth()
    return gauth


def drive_logout() -> None:
    gauth = GoogleAuth()
    cred_file = gauth.settings.get("save_credentials_file")
    token = os.path.join(DIR_PATH, cred_file)
    gauth.LoadCredentials()
    if not gauth.access_token_expired:
        requests.post(url=REVOKE, params={'token': gauth.credentials.access_token},
                      headers={'Content-type': 'application/x-www-form-urlencoded'})
    os.remove(token)
