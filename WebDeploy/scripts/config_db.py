"""
    File            :   config_db.py
    Author          :   Daljeet Singh Chhabra
    Date Created    :   31-08-2020
    Date Modified   :   31-08-2020
"""


class Mongo:
    """
        Class to configure the MongoDB Installation on server
    """

    def __init__(self):
        """
            Downloads and installs MongoDB on the Server
        """
        pass

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
        create_admin = input('Create admin user? [YES] :')
        if create_admin == '' or create_admin.lower() == 'yes':
            if self.create_user(as_admin=True):
                print("> MongoDB Admin created successfully!")
            else:
                print("> Unable to create MongoDB Admin!")

        if self.create_user():
            print("> MongoDB database user created successfully!")
        else:
            print("> Unable to create MongoDB database user!")
