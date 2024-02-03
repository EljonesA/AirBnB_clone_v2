#!/usr/bin/python3
""" Fabric script that distributes an archive to your web servers """
from fabric.api import *
from datetime import datetime
import os


# hostname / IP of the servers
env.hosts = ['34.232.53.204', '54.145.155.223']
env.user = "ubuntu"


def do_deploy(archive_path):
    """
    Distributes an archive to web servers and create new sym link
    """
    # check if archive exists
    if not os.path.exists(archive_path):
        return False
    try:
        # upload archive to server /tmp
        put(local=archive_path, remote="/tmp")

        # Uncompress the archive to the folder
        archive_filename = os.path.basename(archive_path)
        archive_filename_no_ext = os.path.splitext(archive_filename)[0]
        archive_dest_folder = f'/data/web_static/releases/{archive_filename_no_ext}'
        run(f"mkdir -p {archive_dest_folder}")
        run(f"tar -xzf /tmp/{archive_filename} -C {archive_dest_folder}")

        # delete archive from server
        run(f"rm /tmp/{archive_filename}")

        # delete symbolic link
        sym_link = "/data/web_static/current"
        run(f"rm -rf {sym_link}")

        # Create a new the symbolic link /data/web_static/current on the web server
        run(f"sudo ln -s {archive_dest_folder} /data/web_static/current")

        return True
    except Exception as e:
        return False