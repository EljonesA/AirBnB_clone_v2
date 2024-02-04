#!/usr/bin/python3
"""
Fabric script that creates and distributes an archive to your web servers
"""
from fabric.api import local, put, run, env, lcd
from datetime import datetime
import os


# hostname / IP of the servers
env.hosts = ['34.232.53.204', '54.145.155.223']
env.user = "ubuntu"


def do_pack():
    """
    create .tgz archive using tar command
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


def do_deploy(archive_path):
    """
    Distributes an archive to web servers and create new sym link
    """
    # check if archive exists
    if not os.path.exists(archive_path):
        return False
    try:
        # Extract the archive filename without extension
        path = archive_path.split('/')[-1]
        path_no_ext = path.strip('.tgz')

        # Define the destination path for the release
        releases_path = "/data/web_static/releases/{}/".format(path_no_ext_)

        # upload archive to server /tmp
        put(archive_path, "/tmp")

        # Create the directory for the release
        run("mkdir -p {}".format(releases_path))


         # Extract the archive to the release directory
        run("tar -xzf {} -C {}".format(path, releases_path))

        # Remove the temporary archive
        run("rm {}".format(path))

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
    except:
        return False


def deploy():
    """
    Deploy the web static content using do_pack & do_deploy functions
    """
    # Create the archive
    archive_path = do_pack()
    if archive_path is None:
        return False
    # Deploy the archive
    return do_deploy(archive_path)


def do_clean(number=0):
    """
    Deletes out-of-date archives
    """
    # Convert number to int
    number = int(number)

    # Ensure that at least one archive is kept
    if number < 1:
        number = 1

    # Remove out-of-date archives from the local 'versions' folder
    with lcd('versions'):
        local('ls -t | tail -n +{} | '
              'xargs -I {{}} rm -- {{}}'.format(number + 1))

    # Remove out-of-date archives from the remote '/data/web_static/releases' folder
    with cd('/data/web_static/releases'):
        run('ls -t | tail -n +{} | '
            'xargs -I {{}} rm -rf -- {{}}'.format(number + 1))