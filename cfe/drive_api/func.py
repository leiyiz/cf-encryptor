from typing import List

from pydrive2.auth import GoogleAuth
from pydrive2.drive import GoogleDrive

from auth import drive_login


def init_folder():
    create_folder(['cfe'])


def file_list(folder_path: List[str], auth: GoogleAuth = None):
    """
    list all files under given folder

    :param folder_path: a list of strings representing the path to a folder (inclusive) on the drive
    :return: list of GoogleDriveFile objects from which metadata like f['title'] and f['id'] can be read
    """
    pass


def file_replace(file_path: str, folder_path: List[str], auth: GoogleAuth = None):
    """
    upload file from local to gDrive, if a file with same "title" already exists, replace that file.

    :param file_path: local path of file needs to be uploaded
    :param folder_path: a list of strings representing the path to the target folder (inclusive) on the drive
    :return: fid of uploaded file
    """
    pass


def file_upload(file_path: str, auth: GoogleAuth = None):
    gauth = auth if not auth else drive_login()
    drive = GoogleDrive(gauth)

    file = drive.CreateFile()
    file.SetContentFile(file_path)
    file.Upload()


def file_download(file_name: str, folder_path: List[str], target_path: str, auth: GoogleAuth = None):
    """

    :param file_name: name of the file to be downloaded
    :param folder_path: a list of strings representing the path to a gDrive folder containing
           source file (inclusive) on the drive
    :param target_path: local path to which the file be downloaded
    """
    pass


def file_download_by_id(fid: str, target_path: str, auth: GoogleAuth = None):
    gauth = auth if auth else drive_login()
    drive = GoogleDrive(gauth)

    file = drive.CreateFile({'id': fid})
    file.GetContentFile(target_path)


def create_folder(folder_path: List[str] = None, auth: GoogleAuth = None):
    """
    create a folder if it does not exist yet, otherwise just returns the fid
    :param folder_path: a list of strings representing the path to the folder (inclusive) to be created
    :return: fid of the folder matching the folder_path
    """
    pass
