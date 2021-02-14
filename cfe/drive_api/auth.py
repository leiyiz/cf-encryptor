import os

import requests
import yaml
from pydrive2.auth import GoogleAuth

DIR_PATH = os.path.dirname(os.path.realpath(__file__))
REVOKE = "https://accounts.google.com/o/oauth2/revoke"
SETTINGS_FILE = os.path.join(DIR_PATH, 'settings.yaml')


def drive_login(drive_name: str) -> GoogleAuth:
    cwd = change_dir()  # temp solution until we know what will be the working directory

    setting_file = config_exist(drive_name, True)
    gauth = GoogleAuth(settings_file=setting_file)
    gauth.LocalWebserverAuth()

    os.chdir(cwd)

    return gauth


def drive_logout(drive_name: str) -> None:
    cwd = change_dir()

    setting_file = config_exist(drive_name, True)
    gauth = GoogleAuth(settings_file=setting_file)
    cred_file = gauth.settings.get("save_credentials_file")
    token = os.path.join(DIR_PATH, cred_file)
    gauth.LoadCredentials()
    if not gauth.access_token_expired:
        print('logging out from the gDrive...')
        requests.post(url=REVOKE, params={'token': gauth.credentials.access_token},
                      headers={'Content-type': 'application/x-www-form-urlencoded'})
    os.remove(token)

    os.chdir(cwd)


# util

def change_dir() -> str:
    cwd = os.getcwd()
    os.chdir(DIR_PATH)
    return cwd


def config_change(drive_name: str, save_cred: bool = True):
    config_name = config_exist(drive_name, True)
    with open(config_name, 'r') as file:
        data = yaml.load(file, Loader=yaml.FullLoader)

    data['save_credentials'] = save_cred

    with open(config_name, 'w') as file:
        yaml.dump(data, file, default_flow_style=False)


def config_exist(drive_name: str, create_if_not_exist: bool = False) -> str:
    config_name = drive_name + '_settings.yaml'

    if not os.path.exists(config_name):
        print(f'config file {config_name} does not exist in path {os.getcwd()}')
        if not create_if_not_exist:
            exit(1)

    data = {'client_config_file': 'client_secret.json',
            'save_credentials': True,  # change to false if user specified to not save cred
            'save_credentials_backend': 'file',
            'save_credentials_file': drive_name + '_token.json',
            'oauth_scope':
                ['https://www.googleapis.com/auth/drive']}

    with open(config_name, 'w') as file:
        yaml.dump(data, file, default_flow_style=False)

    return config_name
