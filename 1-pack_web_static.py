#!/usr/bin/python3
"""
Fabric script that generates a .tgz archive from the contents of the web_static
folder of the AirBnB Clone repo
"""

from datetime import datetime
from fabric.api import local
from os.path import isdir


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

