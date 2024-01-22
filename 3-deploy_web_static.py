#!/usr/bin/python3
# fab file to archive a directory and deploy it on a server

"""Archives and deploys a local directory to a server."""

from fabric.api import *
from datetime import datetime
import os


env.hosts = ['ubuntu@54.160.104.92', 'ubuntu@52.23.212.44']
archive = ''


def do_pack():

    """Creates and stores the archive of a directory."""

    global archive
    date_time = datetime.now().strftime('%Y%m%d%H%M%S')
    archive = "versions/web_static_{}.tgz".format(date_time)
    local('mkdir -p versions')
    local('tar -czvf {} web_static'.format(archive))
    result = os.path.exists(archive)

    if result is False:
        return None
    else:
        file_size = os.path.getsize(archive)
        print("web_static packed: {} -> {}Bytes".format(archive, file_size))
        return True


def do_deploy(archive_path):

    """deploys the web_static files on the server."""

    tmp_archive_name = archive_path[9:]  # archive name with .tgz
    archive_name = tmp_archive_name[:-4]  # archive name without .tgz
    tmp_archive_dir = '/tmp/{}'.format(tmp_archive_name)
    remote_archive_dir = '/data/web_static/releases/{}/'.format(archive_name)
    SYMLINK = '/data/web_static/current'

    if os.path.exists(archive_path) is False:
        return False

    try:
        put(archive_path, '/tmp/', use_sudo=True)
        run('mkdir -p {}'.format(remote_archive_dir))
        run('tar -xzf {} -C {}'.format(tmp_archive_dir, remote_archive_dir))
        run('rm {}'.format(tmp_archive_dir))
        run('mv {}web_static/* {}'.format(remote_archive_dir,
                                          remote_archive_dir))
        run('rm -rf {}web_static/'.format(remote_archive_dir))
        run('rm -rf {}'.format(SYMLINK))
        run('ln -s {} {}'.format(remote_archive_dir, SYMLINK))
        print("New version deployed!")
        return True
    except Exception as e:
        return False


def deploy():

    """Controls the creating and deploying of the archive to the server."""

    result_pack = do_pack()
    if result_pack is None:
        return False
    else:
        result_deploy = do_deploy(archive)
        return result_deploy
