#!/usr/bin/python3
# Fabric script to archive a directory, then transfer and
# dearchive it in a server.

"""Script to deploy a static on a server using fabric."""

from fabric.api import *
from datetime import datetime
import os


def do_pack():

    """Creates and stores the archive of a directory."""

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
