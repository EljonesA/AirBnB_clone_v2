#!/usr/bin/env/python3
"""Function that deletes out-of-date archives"""
from fabric.api import *


# hostname / IP of the servers
env.hosts = ['34.232.53.204', '54.145.155.223']
env.user = "ubuntu"


def do_clean(number=0):
    """Cleans up outdated archives"""

    try:
        number = int(number)
        if number < 0:
            number = 0

        # Increment number by 1 to keep the most recent ones
        number += 1

        # Clean up local archives
        local('ls -t versions | tail -n +{} | xargs -I {{}} rm versions/{{}}'.format(number))

        # Clean up remote archives
        path = '/data/web_static/releases'
        run('ls -t {} | tail -n +{} | xargs -I {{}} rm -rf {}/{{}}'.format(path, number, path))

        return True
    except Exception as e:
        print("Error:", e)
        return False