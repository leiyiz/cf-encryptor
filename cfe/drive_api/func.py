from pydrive2.drive import GoogleDrive

from .auth import drive_login


# TODO: file listing and drive navigation so that we can specify where to upload & download from

def file_upload(file_path: str):
    gauth = drive_login()
    drive = GoogleDrive(gauth)

    # TODO: need to check if the file already exist on google drive
    file = drive.CreateFile()
    file.SetContentFile(file_path)
    file.Upload()


def file_download_by_id(fid, target_path):
    gauth = drive_login()
    drive = GoogleDrive(gauth)

    file = drive.CreateFile({'id': fid})
    file.GetContentFile(target_path)
