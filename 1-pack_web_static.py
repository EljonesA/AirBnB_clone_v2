#!/usr/bin/python3
""" Fabric script that generates a .tgz archive from contents of a folder """
from fabric.api import local
from datetime import datetime
import os


def do_pack():
    """
    create .tgz archive using tar command
    command takes 3 argurments:
        tar -czvf archive_name.tgz files/folder_to_archive
    Options:
        c - create archive
        z - use gzip to compress the files
        v - list files processed
        f - specifies name of the archive file
    """
    try:
        # create archive path/name with date and time for versions
        now = datetime.now()
        time_format = now.strftime("%Y%m%d%H%M%S")
        archive_path = "versions/web_static_{}.tgz".format(time_format)

        # create new dir if it doesn't already exist
        if not os.path.exists("versions"):
            local("mkdir versions")

        # create .tgz archive using tar command
        local("tar -czvf {} web_static".format(archive_path))
        # check if archive correctly generated
        if os.path.exists(archive_path):
            return archive_path
    except:
        return None