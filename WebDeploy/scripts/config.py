"""
    File            :   config.py
    Author          :   Daljeet Singh Chhabra
    Date Created    :   05-07-2020
    Date Modified   :   04-09-2020
"""
import os
import subprocess


class SystemConfig:
    """
        Class to configure the system for deployment
    """

    def __init__(self):
        self.project_directory = os.getcwd()
        self.project_name = input(
            'Enter project name without spaces [{}]: '.format(self.project_directory.split('/')[-1]))
        if self.project_name == '':
            self.project_name = self.project_directory.split('/')[-1]
        self.pip = 'pip'

    def config_env(self):
        """
            Installing major dependencies to deploy the flask project.
        :return:
        """
        print('Installing dependencies for {}...'.format(self.project_name))
        with open(self.project_name + '-deployment.log', 'a') as dep_log:
            subprocess.run(['sudo', 'apt-get', 'update'], stdout=dep_log, stderr=subprocess.STDOUT)
            # Installing the python3-venv package
            subprocess.run(['sudo', 'apt', 'install', '-y', 'python3-venv'], stdout=dep_log, stderr=subprocess.STDOUT)
            # Installing nginx
            print('> Installing NGINX')
            subprocess.run(['sudo', 'apt', 'install', '-y', 'nginx'], stdout=dep_log, stderr=subprocess.STDOUT)
            # Setting Firewall
            print('> Configuring firewall')
            subprocess.run(['sudo', 'ufw', 'allow', 'Nginx HTTP'], stdout=dep_log, stderr=subprocess.STDOUT)
            subprocess.run(['sudo', 'ufw', 'allow', 'OpenSSH'], stdout=dep_log, stderr=subprocess.STDOUT)
            subprocess.run(['sudo', 'ufw', '-f', 'enable'], stdout=dep_log, stderr=subprocess.STDOUT)
        print('Successfully installed dependencies for {}...'.format(self.project_name))

    def select_project_directory(self):
        """
            Select the project directory
        :return:
        """
        directory = input('Enter full path to the project directory [{}]: '.format(self.project_directory))
        if directory == '':
            directory = self.project_directory

        if os.path.isdir(directory):
            if directory != '':
                self.project_directory = directory
                print('> Selecting directory ({}) as the project directory '.format(self.project_directory))
            else:
                print('> Selecting current directory ({}) as the project directory '.format(self.project_directory))
        else:
            print('> Entered path \'{}\' does not exist..'.format(directory))
            self.select_project_directory()
            return

    def create_venv(self):
        """
            Create virtual environment in the project directory.
        :return:
        """
        print('Creating virtual environment for {}'.format(self.project_name))
        with open(self.project_name + '-deployment.log', 'a') as dep_log:
            subprocess.run(['python3', "-m", "venv", "{}/venv".format(self.project_directory)],
                           stdout=dep_log, stderr=subprocess.STDOUT)
            print('> Created venv for {}...'.format(self.project_name))
        self.pip = os.path.join(self.project_directory, 'venv', 'bin', 'pip')

    def setup_venv(self):
        """
            Setting up Flask Virtual Environment
        :return:
        """
        requirements = input('Enter name of requirements file [requirements.txt]: ')
        if requirements == '':
            requirements = 'requirements.txt'
        requirements_path = os.path.join(self.project_directory, requirements)

        if not os.path.exists(requirements_path):
            print('> Requirements file \'{}\' does not exist in project directory.'
                  '\n...Ensure the file name or create the file \'{}\' in the project directory...'.format(requirements,
                                                                                                           requirements))
            self.setup_venv()
            return

        print('> Installing requirements from {}'.format(requirements))
        with open(self.project_name + '-deployment.log', 'a') as dep_log:
            subprocess.run([self.pip, "install", "wheel"], stdout=dep_log, stderr=subprocess.STDOUT)
            subprocess.run([self.pip, "install", "gunicorn"], stdout=dep_log, stderr=subprocess.STDOUT)
            subprocess.run([self.pip, "install", "-r", requirements_path], stdout=dep_log, stderr=subprocess.STDOUT)

    def get_project_details(self):
        """
            Function to return project details.
        :return: Dict
        """
        data = {
            'project_name': self.project_name,
            'project_directory': self.project_directory,
            'pip': self.pip
        }
        return data


def execute_system_config():
    """
        Function to execute system config commands
    :return: Dict of project details
    """
    run = SystemConfig()
    print('Starting to configure system for deployment...')
    run.config_env()
    run.select_project_directory()
    run.create_venv()
    run.setup_venv()
    print('~~~~~~~~~~~~~~~System Configuration Complete~~~~~~~~~~~~~~~\n')
    return run.get_project_details()
