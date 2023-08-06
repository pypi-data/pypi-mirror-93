# -*- coding: utf-8 -*-
"""Various tools for TA."""
import logging
import os
import re
from pathlib import Path


def get_unique_email_handles(path):
    """
    Return unique email handle in folder of submitted files.

    :param path: A path to folder containing files extracted from downlaoded zip file.
    :type path: str, pathlib.Path
    :return: List of unique email handles.
    :rtype: list[str]
    :raises ValueError: When path is not a directory.
    """

    if isinstance(path, str):
        path = Path(path)

    if not path.is_dir():
        raise ValueError(f"path ({path}) need to be a directory.")

    email_handle_pattern = re.compile(r"_(?P<email_handle>..\d{6})_attempt_")

    # Get all files.
    files = [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]

    email_handles = []
    # Extract handles.
    for name in files:
        res = email_handle_pattern.findall(name)

        if len(res) != 0:
            email_handles.append(res[0])

    unique_email_handles = list(set(email_handles))

    return unique_email_handles


def categorize(source, destination):
    """
    Group files from the same student together in a folder.

    Pre-condition: A root_directory is the result of the
    extracting a files out from the archive file from Blackboard.

    Post-condition: In the destination folder, folders for each student
    will be created, and a file will be moved into its corresponding
    folder.

    :param source: A path to source directory.
    :type source: str, pathlib.Path

    :param destination: A path to destination directory.
    :type destination: str, pathlib.Path

    :raises ValueError: When path is not a directory.
    """

    if isinstance(source, str):
        source = Path(source)
    if isinstance(destination, str):
        destination = Path(destination)

    if (not source.is_dir()) or (not destination.is_dir()):
        raise ValueError(
            f"source ({source}) or destination ({destination}) or both is not a directory"
        )

    email_handle_pattern = re.compile(r"_(?P<email_handle>..\d{6})_attempt_")
    filename_pattern = re.compile(
        r"_attempt_(?:\d{4}-\d{2}-\d{2}-\d{2}-\d{2}-\d{2})*(?P<filename>.*)"
    )

    # Get list of student email handles.
    unique_email_handles = get_unique_email_handles(source)

    # Create destination if not exist.
    if not os.path.exists(destination):
        os.mkdir(destination)

    # Create folders in the destination.
    for email_handle in unique_email_handles:
        if not os.path.exists(os.path.join(destination, email_handle)):
            os.mkdir(os.path.join(destination, email_handle))

    # Renaming and move files into directory.
    files = [f for f in os.listdir(source) if os.path.isfile(os.path.join(source, f))]
    for raw_filename in files:
        logging.info(f"raw file name: {raw_filename}")

        # Renaming.
        res = filename_pattern.findall(raw_filename)

        if len(res) != 0:
            filename = res[0]

        logging.info(f"file name: {filename}")

        new_filename = ""
        if filename == ".txt":
            new_filename = "_bb_note.txt"
        else:
            new_filename = filename[1:]

        logging.info(f"new file name: {new_filename}")

        # Get email handle.
        email_handle = email_handle_pattern.findall(raw_filename)[0]

        # Move file
        try:
            os.rename(
                os.path.join(source, raw_filename),
                os.path.join(destination, email_handle, new_filename),
            )
        except OSError as ex:
            logging.error("{}".format(raw_filename))
