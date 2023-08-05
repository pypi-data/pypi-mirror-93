from setuptools import setup

setup(
    name = "GoogleDriveUpload",
    version = "1.0.0",
    author = "yoshida",
    author_email = "yoshida.pypi@gmail.com",
    url = "https://github.com/yoshida121/GoogleDriveUpload",
    description = "File or Folder Upload to Google Drice.",
    long_description = """
    Upload files and folders from Python to Google Drive.
    This library allows recursive folder search.
    From now on, it will support file search and file download of Google Drive.
    """,
    install_requires = [
        "pydrive"
    ]
)