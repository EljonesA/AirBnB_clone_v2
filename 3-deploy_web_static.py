#!/usr/bin/python3
"""
Fabric script that creates and distributes an archive to your web servers
"""
from fabric.api import local, put, run, env
from os.path import exists
from datetime import datetime


# hostname / IP of the servers
env.hosts = ['34.232.53.204', '54.145.155.223']
env.user = "ubuntu"


def do_pack():
    """
    Create a compressed archive of web_static folder
    """
    try:
        # Create folder if it doesn't exist
        local("mkdir -p versions")
        # Create archive file name with current date and time
        time_format = datetime.now().strftime("%Y%m%d%H%M%S")
        file_name = "versions/web_static_{}.tgz".format(time_format)
        # Create the archive
        local("tar -cvzf {} web_static".format(file_name))
        return file_name
    except:
        return None


def do_deploy(archive_path):
    """
    Distribute archive to web servers and create symbolic link
    """
    if not exists(archive_path):
        return False

    try:
        # Upload archive to /tmp/ directory
        put(archive_path, "/tmp/")
        # Extract archive to /data/web_static/releases/
        archive_name = archive_path.split('/')[-1]
        archive_name_no_ext = archive_name.split('.')[0]
        run("mkdir -p /data/web_static/releases/{}/".format(archive_name_no_ext))
        run("tar -xzf /tmp/{} -C /data/web_static/releases/{}/"
            .format(archive_name, archive_name_no_ext))
        # Delete uploaded archive
        run("rm /tmp/{}".format(archive_name))
        # Move contents of extracted folder to its parent directory
        run("mv /data/web_static/releases/{}/web_static/* /data/web_static/releases/{}/"
            .format(archive_name_no_ext, archive_name_no_ext))
        # Remove empty folder
        run("rm -rf /data/web_static/releases/{}/web_static".format(archive_name_no_ext))
        # Delete old symbolic link if exists
        run("rm -rf /data/web_static/current")
        # Create new symbolic link
        run("ln -s /data/web_static/releases/{}/ /data/web_static/current"
            .format(archive_name_no_ext))
        print("New version deployed!")
        return True
    except:
        return False


def deploy():
    """
    Deploy the web static content
    """
    # Create the archive
    archive_path = do_pack()
    if archive_path is None:
        return False
    # Deploy the archive
    return do_deploy(archive_path)