#!/usr/bin/python3
"""
Write a Fabric script (based on the file 1-pack_web_static.py) that
distributes an archive to your web servers, using the function do_deploy
"""
from fabric.api import local, run, env, put
from fabric.contrib.files import exists
from datetime import datetime
import os


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
    """
    function that distribute an archive to web servers
    Args: archive_path(str) the path to file
    returns: true if all operations have been successful
    """

    if not exists(archive_path):
        return False

    try:
        """ updating the archive to the tmp file"""
        put(archive_path, '/tmp/')

        """
        Extracting the archive to data/web/releases/filename without
        extension
        """
        archive_filename = archive_path.split("/")[-1]
        folder_name = archive_filename.split(".")[0]
        release_path = f'/data/web_static/releases/{folder_name}'
        run(f'mkdir -p {realease_path}')
        run(f'tar -xzf /tmp/{archive_filename} -C {release_path}')
        """ delete the archive from the webserver"""
        run(f'rm /tmp/{archive_filename}')

        """ delete symbolic link /data/web_static/current"""
        run('rm -rf /data/web_static/current')

        """create a new symbolic link /data/webstatic/current"""
        run(f'ln -s {release_path} /data/web_static/current')
        print("New version deployed!")
        return True
    except Exception as e:
        return False
