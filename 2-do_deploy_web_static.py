#!/usr/bin/python3
""" Fabric script for creating archive from github repos"""
from fabric.api import local, put, env, run, sudo
from datetime import datetime
import os
env.hosts = [
    '3.85.54.241',
    '52.86.86.171'
]


def do_pack():
    """creates a tgz archive from the current folder"""
    local("mkdir -p versions")
    out_name = f"web_static_{datetime.now().strftime('%Y%m%d%H%M%S')}.tgz"
    result = local("tar -cvzf versions/{} web_static".format(out_name),
                   capture=True)
    if not result.return_code:
        return f"versions/{out_name}"
    return None


def do_deploy(archive_path):
    """distributes an archive to webservers"""
    if not os.path.exists(archive_path):
        return False

    basename = os.path.basename(archive_path)
    rem_archive_path = f"/tmp/{basename}"

    try:
        put(archive_path, rem_archive_path)
        x_archive = "/data/web_static/releases/{}".format(
            os.path.splitext(basename)[0]
        )
        run(f"mkdir -p {x_archive}")
        run("tar -xzf {} -C {} --strip-components=1".format(
            rem_archive_path, x_archive
            ))
        run(f"rm -f {rem_archive_path}")
        symlink = "/data/web_static/current"
        run(f"rm -rf {symlink}")
        run(f"ln -s {x_archive} {symlink}")
    except Exception:
        return False

    return True
