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
        # Extract the archive filename
        name = archive_path.replace('/', ' ')
        name = shlex.split(name)
        name = name[-1]

        # Extract the archive filename without extension
        wname = name.replace('.', ' ')
        wname = shlex.split(wname)
        wname = wname[0]

        # Define the destination path for the release
        releases_path = "/data/web_static/releases/{}/".format(wname)
        tmp_path = "/tmp/{}".format(name)

        # upload archive to server /tmp
        put(archive_path, "/tmp")

        # Create the directory for the release
        run("mkdir -p {}".format(releases_path))


         # Extract the archive to the release directory
        run("tar -xzf {} -C {}".format(tmp_path, releases_path))

        # Remove the temporary archive
        run("rm {}".format(tmp_path))

        # Move the contents of the extracted folder to the release directory
        run("mv {}web_static/* {}".format(releases_path, releases_path))

        # Remove the extracted folder
        run("rm -rf {}web_static".format(releases_path))

        # Remove the current symbolic link
        run("rm -rf /data/web_static/current")

        # Create a new symbolic link pointing to the new release
        run("ln -s {} /data/web_static/current".format(releases_path))

        print("New version deployed!")
        return True
    except Exception as e:
        return False