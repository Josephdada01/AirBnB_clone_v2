#!/usr/bin/python3
"""Deployment Script Module for Web Static Content"""

import os
from datetime import datetime
from fabric.api import local, run, env, put

"""Define the remote servers"""
env.hosts = ["52.201.229.78", "54.87.205.191"]

def do_pack():
    """
    the fuction will return the archive path if the archive has
    been correctly generated
    """

    """ this create the version folder if it doesnt exists """

    the_path = "versions"
    if not os.path.exists(the_path):
        os.makedirs(the_path)

    """ once the acrchive name is created the time stamp will be there"""
    now = datetime.now()
    time_stamp = now.strftime("%Y%m%d%H%M%S")

    archive_name = "web_static_{}.tgz".format(time_stamp)
    archive_path = "{}/{}".format(the_path, archive_name)

    content = "web_static"

    """running the tar command to create the archive"""

    print("Archive path:", archive_path)
    """This means ouctome 'out' """
    out = local("tar -cvzf {} {}".format(archive_path, content), capture=True)
    print(out.stdout)

    if out.succeeded:
        return archive_path
    return None


def do_deploy(archive_path):
    """Distributes an archive to web servers and deploys it.

    Args:
        archive_path (str): Path to the archive.

    Returns:
        bool: True if deployment is successful, False otherwise.
    """

    """Check if the archive_path exists"""
    if not os.path.exists(archive_path):
        return False

    try:
        """Extract relevant information from the archive path"""
        archived_file = archive_path[9:]
        file_with_no_ext = archived_file[:-4]
        file_dir = "/data/web_static/releases/{}/".format(file_with_no_ext)

        """Prepare the archive for deployment"""
        archived_file = "/tmp/" + archive_path[9:]
        put(archive_path, "/tmp/")
        run("mkdir -p {}".format(file_dir))
        run("tar -xvf {} -C {}".format(archived_file, file_dir))
        run("rm {}".format(archived_file))
        
        """Move files, create symbolic link, and clean up"""
        run("mv {}web_static/* {}".format(file_dir, file_dir))
        run("rm -rf {}web_static".format(file_dir))
        run("rm -rf {}".format("/data/web_static/current"))
        run("ln -s {} /data/web_static/current".format(file_dir))

        print("New version deployed!")
        return True
    except Exception as e:
        return False


def deploy():
    """Create and distribute archive to a web server."""
    file = do_pack()
    if file is None:
        return False
    return do_deploy(file)
