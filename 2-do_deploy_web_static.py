#!/usr/bin/python3
# Fab file to deploy a site to a server

"""script to deploy a file to a server."""

from fabric.api import *
from datetime import datetime
import os


env.hosts = ['ubuntu@54.160.104.92', 'ubuntu@52.23.212.44']


def do_deploy(archive_path):

    """deploys the web_static files on the server."""

    tmp_archive_name = archive_path[9:]  # archive name with .tgz
    archive_name = tmp_archive_name[:-4]  # archive name without .tgz
    tmp_archive_dir = '/tmp/{}'.format(tmp_archive_name)  # temporary directory where archive is kept
    remote_archive_dir = '/data/web_static/releases/{}/'.format(archive_name)
    SYMLINK = '/data/web_static/current'

    if os.path.exists(archive_path) is False:
        return False

    try:
        put(archive_path, '/tmp/', use_sudo=True)
        run('mkdir -p {}'.format(remote_archive_dir))
        run('tar -xzf {} -C {}'.format(tmp_archive_dir, remote_archive_dir))
        run('rm {}'.format(tmp_archive_dir))
        run('mv {}web_static/* {}'.format(remote_archive_dir, remote_archive_dir))
        run('rm -rf {}web_static/'.format(remote_archive_dir))
        run('rm {}'.format(SYMLINK))
        run('ln -s {} {}'.format(remote_archive_dir, SYMLINK))
        print("New version deployed!")
        return True
    except:
        return False
