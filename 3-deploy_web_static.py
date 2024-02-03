#!/usr/bin/python3
""" Fabric script that creates and distributes an archive to web servers """
from fabric import task
from datetime import datetime
from os import path

# hostname / IP of the servers
env.hosts = ['34.232.53.204', '54.145.155.223']
env.user = "ubuntu"


@task
def do_pack(c):
    """
    Create a .tgz archive from the contents of the web_static folder
    """
    try:
        # create archive path/name with date and time for versions
        now = datetime.now()
        time_format = now.strftime("%Y%m%d%H%M%S")
        archive_path = "versions/web_static_{}.tgz".format(time_format)

        # create new dir if it doesn't already exist
        if not path.exists("versions"):
            c.local("mkdir -p versions")

        # create .tgz archive using tar command
        c.local("tar -czvf {} web_static".format(archive_path))

        # check if archive correctly generated
        if path.exists(archive_path):
            return archive_path
    except Exception as e:
        return None


@task
def do_deploy(c):
    """
    Distribute the archive to web servers and create new symbolic link
    """
    archive_path = do_pack(c)
    if not archive_path:
        return False

    try:
        # upload archive to server /tmp
        c.put(local_path=archive_path, remote="/tmp")

        # Uncompress the archive to the folder
        archive_filename = path.basename(archive_path)
        archive_filename_no_ext = path.splitext(archive_filename)[0]
        archive_dest_folder = f'/data/web_static/releases/{archive_filename_no_ext}'
        c.run(f"mkdir -p {archive_dest_folder}")
        c.run(f"tar -xzf /tmp/{archive_filename} -C {archive_dest_folder}")

        # delete archive from server
        c.run(f"rm /tmp/{archive_filename}")

        # delete symbolic link
        sym_link = "/data/web_static/current"
        c.run(f"rm -rf {sym_link}")

        # Create a new the symbolic link /data/web_static/current on the web server
        c.run(f"sudo ln -s {archive_dest_folder} /data/web_static/current")

        return True
    except Exception as e:
        return False


@task
def deploy(c):
    """
    Deploy the web static content to web servers
    """
    return do_deploy(c)