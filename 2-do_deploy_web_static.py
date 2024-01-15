#!/usr/bin/python3
""" Fabric script for creating archive from github repos"""
from fabric.api import local, put, env, run, sudo
from datetime import datetime
import os
env.hosts = [
    '3.85.54.241',
    '52.86.86.171'
]


def do_deploy(archive_path):
    """distributes an archive to webservers"""
    if not os.path.exists(archive_path):
        return False
    fd = archive_path.split("/")[1]
    try:
        put(archive_path, "/tmp/{}".format(fd))
        run("mkdir -p /data/web_static/releases/{}".format(fd))
        run("tar -xzf /tmp/{} -C /data/web_static/releases/{}".format(fd, fd))
        run("rm /tmp/{}".format(fd))
        run("mv /data/web_static/releases/{}/web_static/*\
        /data/web_static/releases/{}/".format(fd, fd))
        run("rm -rf /data/web_static/releases/{}/web_static".format(fd))
        run("rm -rf /data/web_static/current")
        run("ln -s /data/web_static/releases/{}/\
        /data/web_static/current".format(fd))
        print("New version deployed!")
        return True
    except:
        print("Deployment failed!")
        return False
