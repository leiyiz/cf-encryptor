from typing import List

from pydrive2.auth import GoogleAuth
from pydrive2.drive import GoogleDrive

from auth import drive_login

FOLDER_TYPE = 'application/vnd.google-apps.folder'
MIME = 'mimeType'


def init_folder():
    create_folder(['cfe'])


def file_list(folder_path: List[str], auth: GoogleAuth = None):
    """
    list all files under given folder

    :param folder_path: a list of strings representing the path to a folder (inclusive) on the drive
    :return: list of GoogleDriveFile objects from which metadata like f['title'] and f['id'] can be read
    """
    gauth = auth if not auth else drive_login()
    drive = GoogleDrive(gauth)
    folder_id = create_folder(folder_path, gauth)
    return drive.ListFile({
        'q': f"'{folder_id}' in parents and trashed=false"
    }).GetList()


def file_replace(file_name: str, file_path: str, folder_path: List[str], auth: GoogleAuth = None):
    """
    upload file from local to gDrive, if a file with same "title" already exists, replace that file.

    :param file_name: filename recorded on drive e.g. resume.txt
    :param file_path: local absolute path of file needs to be uploaded
    :param folder_path: a list of strings representing the path to the target folder (inclusive) on the drive
    :return: fid of uploaded file
    """
    pass


def file_upload(file_name: str, file_path: str, folder_path: List[str], auth: GoogleAuth = None):
    gauth = auth if not auth else drive_login()
    drive = GoogleDrive(gauth)
    folder_id = create_folder(folder_path)
    upload(file_name, file_path, drive, folder_id)


def file_download(file_name: str, folder_path: List[str], target_path: str, auth: GoogleAuth = None):
    """

    :param file_name: name of the file to be downloaded
    :param folder_path: a list of strings representing the path to a gDrive folder containing
           source file (inclusive) on the drive
    :param target_path: local path to which the file be downloaded
    """
    pass


def create_folder(folder_path: List[str], auth: GoogleAuth = None) -> str:
    """
    create a folder if it does not exist yet, otherwise just returns the fid
    :param folder_path: a list of strings representing the path to the folder (inclusive) to be created
    :return: fid of the folder matching the folder_path
    """
    if len(folder_path) < 1:
        raise ValueError("folder path must has at least 1 value")
    gauth = auth if not auth else drive_login()

    drive = GoogleDrive(gauth)

    parent = 'root'
    for name in folder_path:
        folders = drive.ListFile({
            'q': f"{MIME}='{FOLDER_TYPE}' AND title='{name}' and trashed=false AND '{parent}' in parents"
        }).GetList()
        if len(folders) == 0:  # no such folder
            new_folder = drive.CreateFile({'title': name, MIME: FOLDER_TYPE, 'parents': [{"id": parent}]})
            new_folder.Upload()
            parent = new_folder['id']
        elif len(folders) == 1:
            parent = folders[0]['id']
        else:
            raise ValueError("multiple folders with the same name")
    return parent


# util?
def upload(file_name: str, file_path: str, drive: GoogleDrive, parent_id: str):
    file = drive.CreateFile()
    file.SetContentFile(file_path)
    file['title'] = file_name
    file['parents'] = [{'id': parent_id}]
    file.Upload()


def download_by_id(fid: str, target_path: str, auth: GoogleAuth = None):
    gauth = auth if auth else drive_login()
    drive = GoogleDrive(gauth)

    file = drive.CreateFile({'id': fid})
    file.GetContentFile(target_path)
