#!/usr/bin/python3
"""2-do_deploy_web_static module"""
import os
from datetime import datetime
from fabric.api import local, run, env, put


env.hosts = ["52.201.229.78", "54.87.205.191"]


def do_pack():
    """Fabric script that generates a .tgz archive
    from the contents of the web_static folder of
    your AirBnB Clone repo
    """

    """Check if version dir exits:"""
    path = "versions"
    if not os.path.exists(path):
        os.makedirs(path)

    """Get the current time and date"""
    currentDateAndTime = datetime.now()
    archiveTime = currentDateAndTime.strftime("%Y%m%d%H%M%S")

    """Naming of the archive file"""
    name_of_archive = "web_static_{}.tgz".format(archiveTime)

    archive_path = "{}/{}".format(path, name_of_archive)

    content = "web_static"

    """Using of the tar command"""
    result = local("tar -cvzf {} {}".format(archive_path, content))

    if result.succeeded:
        return archive_path

    return None


def do_deploy(archive_path):
    """Distributes an archive to your web servers,
    using the function do_deploy
    Args:
        archive_path: path to the archive
    Return:
        True if sucessfully and False otherwise.
    """

    """If archive_path does not exit"""
    if not os.path.exists(archive_path):
        return False

    try:
        archived_file = archive_path[9:]

        """Without the extension."""
        file_without_ext = archived_file[:-4]

        """Full path without the extension of the file"""
        file_dir = "/data/web_static/releases/{}/".format(
                file_without_ext)

        """Retrive the file name"""
        archived_file = "/tmp/" + archive_path[9:]

        """Upload to /tmp/ directory of the server"""
        put(archive_path, "/tmp/")

        """Create the directory & Uncompress the file"""
        run("mkdir -p {}".format(file_dir))

        run(
                "tar -xvf {} -C {}".format(
                    archived_file,
                    file_dir
                    )
                )

        """Remove thr archived file"""
        run("rm {}".format(archived_file))

        run("mv {}web_static/* {}".format(file_dir, file_dir))

        run("rm -rf {}web_static".format(file_dir))

        run("rm -rf {}".format("/data/web_static/current"))

        """Create a symbolic link"""
        run("ln -s {} /data/web_static/current".format(file_dir))

        print("New version deployed!")

        return True
    except Exception as e:
        return False
