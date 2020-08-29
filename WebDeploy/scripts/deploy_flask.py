"""
    File            :   deploy_flask.py
    Author          :   Daljeet Singh Chhabra
    Date Created    :   03-07-2020
    Date Modified   :   29-08-2020
"""
import os
from getpass import getuser
import subprocess


class Deploy:
    """
        Class to manage the major deployment tasks
    """

    def __init__(self, project_details):
        self.project_name = project_details['project_name']
        self.project_directory = project_details['project_directory']
        self.pip = project_details['pip']
        self.start_file = 'app.py'
        self.app_name = 'app'

    def create_wsgi(self):
        """
            Function to crete a wsgi.py for the project
        :return:
        """
        start_file = input('Enter name of flask entry point [{}]: '.format(self.start_file))
        if start_file == '':
            start_file = self.start_file

        if not os.path.isfile(os.path.join(self.project_directory, start_file)):
            print('> Entry file \'{}\' does not exist in project directory.'
                  '\n...Ensure the file name or create the file \'{}\' in the project directory...'.format(start_file,
                                                                                                           start_file))
            self.create_wsgi()
            return

        app_name = input('Enter flask app name in entry file [{}]: '.format(self.app_name))
        if app_name == '':
            app_name = self.app_name
        wsgi_file = os.path.join(self.project_directory, 'wsgi.py')
        print('Creating wsgi for {}...'.format(self.project_name))
        with open(wsgi_file, 'w') as wsgi:
            content = 'from {} import {}\n\n' \
                      'if __name__ == "__main__":\n' \
                      '\t{}.run()\n'.format(start_file.split('.')[0], app_name, app_name)
            wsgi.write(content)

    def create_gunicorn_process(self):
        """
            Function to create system service for the project
        :return:
        """
        print('Creating system service for {}...'.format(self.project_name))
        service_path = '/etc/systemd/system/flaskApp_{}.service'.format(self.project_name)
        with open(service_path, 'w') as service:
            env_path = os.path.join(self.project_directory, 'venv', 'bin')
            content = '[Unit]\n' \
                      'Description=Gunicorn instance to serve Flask App {project}\n' \
                      'After=network.target\n\n' \
                      '[Service]\n' \
                      'User={user}\n' \
                      'Group=www-data\n' \
                      'WorkingDirectory={wd}\n' \
                      'Environment="PATH={env}"\n' \
                      'ExecStart={env}/gunicorn --workers 2 --bind unix:{project}.sock -m 007 wsgi:{app}\n\n' \
                      '[Install]\n' \
                      'WantedBy=multi-user.target\n' \
                      ''.format(project=self.project_name, wd=self.project_directory, env=env_path, app=self.app_name,
                                user=getuser())
            service.write(content)
        print('> Project service created')
        with open(self.project_name + '-deployment.log', 'a') as dep_log:
            subprocess.run(['sudo', 'systemctl', 'start', 'flaskApp_{}.service'.format(self.project_name)],
                           stdout=dep_log, stderr=subprocess.STDOUT)
            subprocess.run(['sudo', 'systemctl', 'enable', 'flaskApp_{}.service'.format(self.project_name)],
                           stdout=dep_log, stderr=subprocess.STDOUT)
            subprocess.run(['sudo', 'systemctl', 'status', 'flaskApp_{}.service'.format(self.project_name)],
                           stdout=dep_log, stderr=subprocess.STDOUT)
        print('> System service flaskApp_{}.service started...'.format(self.project_name))

    def create_nginx_proxy(self):
        """
            Function to create nginx proxy
        :return:
        """
        print('Creating nginx configuration file for {}...'.format(self.project_name))
        config_path = '/etc/nginx/sites-available/flaskApp_{}'.format(self.project_name)
        domains = input('Enter the domain names (space separated) on which you have to host the flask app: ')
        with open(config_path, 'w') as config_file:
            content = 'server {{\n' \
                      '    listen      80;\n' \
                      '    server_name {domains};\n' \
                      "    location / {{\n" \
                      '        proxy_pass         "http://unix:/{project_dir}/{project}.sock";\n' \
                      '        proxy_redirect     off;\n' \
                      '        proxy_set_header   Host $host;\n' \
                      '        proxy_set_header   X-Real-IP $remote_addr;\n' \
                      '        fastcgi_read_timeout 300s;\n' \
                      '        proxy_read_timeout 300;\n' \
                      '    }}\n' \
                      '    error_log  /var/log/nginx/flaskApp_{project}.log;\n' \
                      '    access_log /var/log/nginx/flaskApp_{project}_access.log;\n' \
                      '}}\n' \
                      ''.format(domains=domains, project=self.project_name, project_dir=self.project_directory)

            config_file.write(content)
        print('> NGINX config completed...')

        with open(self.project_name + '-deployment.log', 'a') as dep_log:
            subprocess.run(['sudo', 'ln', '-s', '/etc/nginx/sites-available/flaskApp_{}'.format(self.project_name),
                            '/etc/nginx/sites-enabled'], stdout=dep_log, stderr=subprocess.STDOUT)
            subprocess.run(['sudo', 'nginx', '-t'], stdout=dep_log, stderr=subprocess.STDOUT)

            subprocess.run(['sudo', 'systemctl', 'restart', 'nginx'.format(self.project_name)],
                           stdout=dep_log, stderr=subprocess.STDOUT)
        print('> NGINX service restarted...'.format(self.project_name))

    def complete_deploy_process(self):
        """
            Function to mark completion of deployment sequence
        :return:
        """
        print('~~~~~~~~~~~~~~~~Deployment Of {} Completed Successfully~~~~~~~~~~~~~~~'.format(self.project_name))
        print('GoodBye!')


def execute_flask_deploy(project_details):
    """
        Function to execute Deploy sequence
    :return:
    """
    run = Deploy(project_details)
    print('> Starting deployment for {}...'.format(project_details['project_name']))
    run.create_wsgi()
    run.create_gunicorn_process()
    run.create_nginx_proxy()
    run.complete_deploy_process()
