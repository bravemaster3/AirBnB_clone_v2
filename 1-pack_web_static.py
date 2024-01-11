#!/usr/bin/python3
""" Fabric script for creating archive from github repos"""
from fabric.api import local
from datetime import datetime


def do_pack():
    """creates a tgz archive from the current folder"""
    local("mkdir -p versions")
    out_name = f"web_static_{datetime.now().strftime('%Y%m%d%H%M%S')}.tgz"
    result = local("tar -cvzf versions/{} web_static".format(out_name),
                   capture=True)
    if not result.return_code:
        return f"versions/{out_name}"
    return None
