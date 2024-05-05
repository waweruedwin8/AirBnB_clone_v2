#!/usr/bin/python3
"""
Fabric script based on the file 2-do_deploy_web_static.py that creates and
distributes an archive to the web servers
""" 
import os
from fabric.api import env, local, put, run
from datetime import datetime
from os.path import exists, isdir

env.hosts = ['3.90.85.77', '52.205.82.148']
env.key_filename = os.path.expanduser('~/.ssh/id_rsa')


def do_pack():
    """
    Generates a .tgz archive from the contents of the web_static folder
    """
    try:
        # Get current date and time
        now = datetime.now()
        date_time = now.strftime("%Y%m%d%H%M%S")
        
        # Create the versions directory if it doesn't exist
        if not isdir("versions"):
            local("mkdir -p versions")
        
        # Define the file name for the archive
        file_name = "versions/web_static_{}.tgz".format(date_time)
        
        # Create the .tgz archive using tar
        local("tar -cvzf {} web_static".format(file_name))
        
        # Return the archive path if successful
        return file_name
    except Exception as e:
        print("An error occurred:", e)
        return None


def do_deploy(archive_path):
    """distributes an archive to the web servers"""
    if exists(archive_path) is False:
        return False
    try:
        file_n = archive_path.split("/")[-1]
        no_ext = file_n.split(".")[0]
        path = "/data/web_static/releases/"
        put(archive_path, '/tmp/')
        run('mkdir -p {}{}/'.format(path, no_ext))
        run('tar -xzf /tmp/{} -C {}{}/'.format(file_n, path, no_ext))
        run('rm /tmp/{}'.format(file_n))
        run('mv {0}{1}/web_static/* {0}{1}/'.format(path, no_ext))
        run('rm -rf {}{}/web_static'.format(path, no_ext))
        run('rm -rf /data/web_static/current')
        run('ln -s {}{}/ /data/web_static/current'.format(path, no_ext))
        return True
    except:
        return False


def deploy():
    """creates and distributes an archive to the web servers"""
    archive_path = do_pack()
    if archive_path is None:
        return False
    return do_deploy(archive_path)


def do_clean(number=0):
    """
    Deletes out-of-date archives
    """
    try:
        # Convert number to integer
        number = int(number)
        
        # Ensure number is at least 1
        if number < 1:
            number = 1
        
        # Get sorted list of archives in versions folder
        with lcd('versions'):
            local_archives = sorted(local('ls -t', capture=True).split())

        # Delete unnecessary archives in versions folder
        archives_to_delete = local_archives[number:]
        for archive in archives_to_delete:
            local('rm -f {}'.format(archive))

        # Get sorted list of archives in releases folder
        with cd('/data/web_static/releases'):
            archives = sorted(run('ls -t').split())

        # Delete unnecessary archives in releases folder
        archives_to_delete = archives[number:]
        for archive in archives_to_delete:
            run('rm -f {}'.format(archive))

    except Exception as e:
        print("An error occurred:", e)

