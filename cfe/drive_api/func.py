from typing import List, Tuple

from pydrive2.drive import GoogleDrive

from auth import drive_login

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
    drive = _drive_gen()
    return _list_file(folder_path, drive)[1]


def file_replace(file_name: str, file_path: str, folder_path: List[str]) -> None:
    """
    upload file from local to gDrive, if a file with same "title" already exists, replace that file.

    :param file_name: filename recorded on drive e.g. resume.txt
    :param file_path: local absolute path of file needs to be uploaded
    :param folder_path: a list of strings representing the path
                        from root (exclusive) to the target folder (inclusive) on the drive
    :return: fid of uploaded file
    """
    drive = _drive_gen()

    folder_id, files = _list_file(folder_path, drive)

    for file in files:
        if file['title'] == file_name:
            file.Trash()

    _upload(file_name, file_path, drive, folder_id)


def file_upload(file_name: str, file_path: str, folder_path: List[str]) -> None:
    drive = _drive_gen()

    folder_id = _create_or_find_folder(folder_path, drive)
    _upload(file_name, file_path, drive, folder_id)


def file_download(file_name: str, folder_path: List[str], target_path: str):
    """

    :param file_name: name of the file to be downloaded
    :param folder_path: a list of strings representing the path from root (exclusive)
                        to a gDrive folder containingsource file (inclusive) on the drive
    :param target_path: local path to a file to which the file be downloaded
    """
    drive = _drive_gen()

    fid = None
    for file in _list_file(folder_path, drive)[1]:
        if file['title'] == file_name:
            fid = file['id']
            break

    if not fid:
        raise FileNotFoundError(f"file {file_name} is not found under /{'/'.join(folder_path)}")

    file = drive.CreateFile({'id': fid})
    file.GetContentFile(target_path)


def create_folder(folder_path: List[str]) -> str:
    """
    create a folder if it does not exist yet, otherwise just returns the fid
    :param folder_path: a list of strings representing the path
                        from root (exclusive) to the folder (inclusive) to be created
    :return: fid of the folder matching the folder_path
    """
    drive = _drive_gen()
    return _create_or_find_folder(folder_path, drive)


# util?

def _list_file(folder_path: List[str], drive: GoogleDrive) -> Tuple[str, list]:
    folder_id = _create_or_find_folder(folder_path, drive)
    return folder_id, drive.ListFile({
        'q': f"'{folder_id}' in parents and trashed=false"
    }).GetList()


def _create_or_find_folder(folder_path: List[str], drive: GoogleDrive) -> str:
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


def _drive_gen() -> GoogleDrive:
    return GoogleDrive(drive_login())


def _upload(file_name: str, file_path: str, drive: GoogleDrive, parent_id: str) -> None:
    file = drive.CreateFile()
    file.SetContentFile(file_path)
    file['title'] = file_name
    file['parents'] = [{'id': parent_id}]
    file.Upload()
