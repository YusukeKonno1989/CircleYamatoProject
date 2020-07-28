#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys
import const
from sshtunnel import SSHTunnelForwarder

def main():
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'CircleYamatoProject.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':

    if const.EXEC_MODE == 'DEBUG':
        with SSHTunnelForwarder(
        (const.SSH_BASTION_ADDRESS, const.SSH_PORT),
        ssh_pkey=const.SSH_PKEY_PATH,
        ssh_username=const.SSH_USER,
        remote_bind_address=(const.MYSQL_HOST, const.MYSQL_PORT),
        local_bind_address=("0.0.0.0", const.MYSQL_PORT),
        ):
            main()
    else:
        main()