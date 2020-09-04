"""
    File            :   config_db.py
    Author          :   Daljeet Singh Chhabra
    Date Created    :   31-08-2020
    Date Modified   :   04-09-2020
"""
import os
import subprocess
import sys


class Mongo:
    """
        Class to configure the MongoDB Installation on server
    """

    def __init__(self, project_name):
        """
            Downloads and installs MongoDB on the Server
        """
        self.supported_os_dist = ['xenial', 'bionic', 'focal']
        proc = subprocess.run(['lsb_release', '-c'], stdout=subprocess.PIPE)
        self.os_dist = proc.stdout.decode('utf-8').strip().split('\t')[-1]

        # Check for supported ubuntu distribution
        if self.os_dist not in self.supported_os_dist:
            print('Your Ubuntu distribution is not supported. '
                  'Kindly upgrade to the distribution supported by WebDeploy.')
            print('Supported Ubuntu Distributions: ', ', '.join(self.supported_os_dist))
            sys.exit(-1)

        print('Starting installation of MongoDB Community Edition...')
        with open(project_name + '-deployment.log', 'a') as dep_log:
            dep_log.write('Starting installation of MongoDB Community Edition...\n')
            subprocess.run(['sudo', 'apt-get', 'update'], stdout=dep_log, stderr=subprocess.STDOUT)
            # Installing GNUPG dependency for MongoDB
            subprocess.run(['sudo', 'apt-get', 'install', 'gnupg'], stdout=dep_log, stderr=subprocess.STDOUT)
            print('> Importing public key...\n> ', end='')
            # Importing public key
            os.system('wget -qO - https://www.mongodb.org/static/pgp/server-4.4.asc | sudo apt-key add -')
            # Creating list file for MongoDB
            os.system('echo "deb [ arch=amd64,arm64 ] https://repo.mongodb.org/apt/ubuntu {dist}/mongodb-org/4.4 '
                      'multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-4.4.list'.format(dist=self.os_dist))

            print('> Downloading MongoDB...')
            subprocess.run(['sudo', 'apt-get', 'update'], stdout=dep_log, stderr=subprocess.STDOUT)

            # Installing MongoDB
            subprocess.run(['sudo', 'apt', 'install', '-y', 'mongodb-org'], stdout=dep_log,
                           stderr=subprocess.STDOUT)
            print('> Completed downloading MongoDB')
            print('> Starting MongoDB...')
            # Starting mongod daemon
            subprocess.run(['sudo', 'systemctl', 'start', 'mongod'], stdout=dep_log, stderr=subprocess.STDOUT)
            # Enabling mongod service
            subprocess.run(['sudo', 'systemctl', 'enable', 'mongod'], stdout=dep_log,
                           stderr=subprocess.STDOUT)
            print('> MongoDB installation completed...')
            # Installing pymongo
            subprocess.run(['sudo', 'pip3', 'install', 'pymongo'], stdout=dep_log, stderr=subprocess.STDOUT)

    @staticmethod
    def create_user(as_admin=False):
        """
            Create a database user
        :param as_admin: Create the user as admin or not. Defaults -> False
        :return: Bool
        """
        try:
            from pymongo import MongoClient, errors
            client = MongoClient("mongodb://localhost:27017/")
            db_name = 'admin'
            if not as_admin:
                db_name = input('Enter DB name for your app: ')
                db_user = input('Enter DB username: ')
                db_pwd = input('Enter DB password: ')
            else:
                db_user = input('Enter username for Admin: ')
                db_pwd = input('Enter password for Admin : ')

            db = client[db_name]
            roles = [{
                'role': 'readWrite',
                'db': db_name,
            }]
            if as_admin:
                roles[0]['role'] = 'userAdminAnyDatabase'

            command_data = {
                "createUser": db_user,
                "pwd": db_pwd,
                "roles": roles
            }
            try:
                db.command(command_data)
                return True
            except errors.OperationFailure:
                print('Entered username {} already exist'.format(db_user))
                return False
        except ImportError:
            print('PyMongo is not installed')
            return False

    def config_mongo(self):
        """
            Configure the MongoDB installation and create database users
        :return:
        """
        print('> Starting MongoDB configuration...')
        create_admin = input('Do you want to create MongoDB admin user? [YES] :')
        if create_admin == '' or create_admin.lower() == 'yes':
            if self.create_user(as_admin=True):
                print("> MongoDB Admin created successfully!")
            else:
                print("> Unable to create MongoDB Admin!")

        if self.create_user():
            print("> MongoDB database user created successfully!")
        else:
            print("> Unable to create MongoDB database user!")


def install_db(choice, project_name):
    # For MongoDB
    if choice == 1:
        db = Mongo(project_name)
        db.config_mongo()
    else:
        return False


def execute_db_config(project_name):
    """
        Function to execute database config
    :param project_name: Name of the project
    :return:
    """
    supported_databases = {
        '1': 'MongoDB',
    }
    failed_attempts = 0
    while True:
        install = input('Do you want to install database for your application? [YES/NO] : ')
        if install.lower() == 'yes':
            print('Supported databases: ')
            for k, v in supported_databases.items():
                print(k, '. ', v, sep='')
            db_choice = input('Enter database number: ')
            if supported_databases.get(db_choice, False):
                install_db(int(db_choice), project_name)
                print('\n~~~~~~~~~~~~~~~Database Configuration Complete~~~~~~~~~~~~~~~\n')
                break
            else:
                print('> Invalid choice... Skipping database installation for', project_name)
                break
        elif install.lower() == 'no':
            print('> Skipping database installation for ', project_name)
            break
        else:
            print('~ INVALID INPUT!')
            failed_attempts += 1
        if failed_attempts == 3:
            print('> Skipping database installation for ', project_name)
            break
