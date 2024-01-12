#!/usr/bin/python3
"""
a Fabric script that generates a .tgz archive from the contents of the
web_static folder of your AirBnB Clone repo, using the function do_pack.
"""
from fabric.api import local
from datetime import datetime
import os


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
    outcome = local("tar -cvzf {} {}".format(archive_path, content), capture=True)
    print(outcome.stdout)

    if outcome.succeeded:
        return archive_path
    return None
