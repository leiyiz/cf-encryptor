import os
from typing import List, Tuple, Optional

from pydrive2.drive import GoogleDrive

from .auth import drive_login

FOLDER_TYPE = 'application/vnd.google-apps.folder'
MIME = 'mimeType'


def init_folder(folder_name: str) -> str:
    return create_folder([folder_name])


def file_list(folder_path: List[str]) -> list:
    """
    list all files under given folder

    :param folder_path: a list of strings representing the path
                        from root (exclusive) to a folder (inclusive) on the drive
    :return: list of GoogleDriveFile objects from which metadata like f['title'] and f['id'] can be read
    """
    drive = __drive_gen()
    return __list_file(folder_path, drive)[1]


def file_replace(file_name: str, file_content: Optional[str], folder_path: List[str]) -> None:
    """
    upload file from local to gDrive, if a file with same "title" already exists, replace that file.

    :param file_name: filename recorded on drive e.g. resume.txt
    :param file_content: string content of file needs to be uploaded
    :param folder_path: a list of strings representing the path
                        from root (exclusive) to the target folder (inclusive) on the drive
    :return: fid of uploaded file
    """
    drive = __drive_gen()

    folder_id, files = __list_file(folder_path, drive)

    for file in files:
        if file['title'] == file_name:
            file.Trash()

    __upload(file_name, file_content, drive, folder_id)


def file_upload(file_name: str, file_content: Optional[str], folder_path: List[str]) -> None:
    drive = __drive_gen()

    folder_id = __create_or_find_folder(folder_path, drive)
    __upload(file_name, file_content, drive, folder_id)


def file_download(file_name: str, folder_path: List[str]) -> bytes:
    """

    :param file_name: name of the file to be downloaded
    :param folder_path: a list of strings representing the path from root (exclusive)
                        to a gDrive folder containingsource file (inclusive) on the drive
    :return: content of downloaded file as string
    """
    drive = __drive_gen()

    fid = None
    for file in __list_file(folder_path, drive)[1]:
        if file['title'] == file_name:
            fid = file['id']
            break

    if not fid:
        raise FileNotFoundError(f"file {file_name} is not found under /{'/'.join(folder_path)}")

    file = drive.CreateFile({'id': fid})
    return file.GetContentIOBuffer().read()


def create_folder(folder_path: List[str]) -> str:
    """
    create a folder if it does not exist yet, otherwise just returns the fid
    :param folder_path: a list of strings representing the path
                        from root (exclusive) to the folder (inclusive) to be created
    :return: fid of the folder matching the folder_path
    """
    drive = __drive_gen()
    return __create_or_find_folder(folder_path, drive)


def file_delete(file_name: str, folder_path: List[str]):
    """
    delete a file if it exists, raise exception if file not found
    :param file_name: name of the file to be deleted
    :param folder_path: a list of strings representing the path from root (exclusive)
                        to a gDrive folder containingsource file (inclusive) on the drive
    """
    drive = __drive_gen()
    deleted = False
    folder_id, files = __list_file(folder_path, drive)
    for file in files:
        if file['title'] == file_name:
            file.Trash()
            deleted = True
    if not deleted:
        raise FileNotFoundError(f"file {file_name} is not found under /{'/'.join(folder_path)}")


# util?

def __list_file(folder_path: List[str], drive: GoogleDrive) -> Tuple[str, list]:
    folder_id = __create_or_find_folder(folder_path, drive)
    return folder_id, drive.ListFile({
        'q': f"'{folder_id}' in parents and trashed=false"
    }).GetList()


def __create_or_find_folder(folder_path: List[str], drive: GoogleDrive) -> str:
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


def __drive_gen() -> GoogleDrive:
    return GoogleDrive(drive_login())


def __upload(file_name: str, file_content: str, drive: GoogleDrive, parent_id: str) -> None:
    file = drive.CreateFile()
    if file_content:
        file.SetContentString(file_content)
    else:
        file.SetContentFile(file_name)
    file['title'] = file_name
    file['parents'] = [{'id': parent_id}]
    file.Upload()
