"""
    File            :   runner.py
    Author          :   Daljeet Singh Chhabra
    Date Created    :   03-07-2020
    Date Modified   :   05-07-2020
"""

from .deploy_flask import execute_flask_deploy
from .deploy_django import execute_django_deploy
from .config import execute_system_config
import os
import sys


def deploy_flask():
    """
        Function to start automatic deployment of flask app
    :return:
    """
    if os.geteuid() != 0:
        os.execvp('sudo', ['sudo', 'python3'] + sys.argv)
    project_details = execute_system_config()
    execute_flask_deploy(project_details)


def deploy_django():
    """
        Function to start automatic deployment of flask app
    :return:
    """
    if os.geteuid() != 0:
        os.execvp('sudo', ['sudo', 'python3'] + sys.argv)
    project_details = execute_system_config()
    execute_django_deploy(project_details)
