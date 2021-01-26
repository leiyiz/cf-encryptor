import os

from drive_api.auth import drive_login, drive_logout
from drive_api.func import file_upload, file_download_by_id

"""
just a script to make sure that simple uploading and downloading works
you can play try running it and remember to replace the fid with something
you have
"""
fid_of_some_pdf_on_your_drive = '1qVxrKKueMZXQdGlrXTVOjEERmiJQ9gj1'

print(f'the current working place is: {os.path.dirname(os.path.realpath(__file__))}')

drive_login()

file_upload('script.py')

file_download_by_id(fid_of_some_pdf_on_your_drive, 'test.pdf')

# drive_logout()
