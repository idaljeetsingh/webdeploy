"""
    File            :   deploy_django.py
    Author          :   Daljeet Singh Chhabra
    Date Created    :   03-07-2020
    Date Modified   :   06-07-2020
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

    def initial_setup(self):
        """
            Function for database migrations and static collection.
        :return:
        """
        v_python = os.path.join(self.project_directory, 'venv', 'bin', 'python')
        manage = os.path.join(self.project_directory, 'manage.py')
        with open(self.project_name + '-deployment.log', 'a') as dep_log:
            print('> Setting up database')
            subprocess.run([v_python, manage, 'makemigrations'], stdout=dep_log, stderr=subprocess.STDOUT)
            subprocess.run([v_python, manage, 'migrate'], stdout=dep_log, stderr=subprocess.STDOUT)
            print('> Collecting static files')
            subprocess.run([v_python, manage, 'collectstatic'], stderr=subprocess.STDOUT)

    def create_gunicorn_process(self):
        """
            Function to create system service for the django project
        :return:
        """
        print('Creating system service for {}...'.format(self.project_name))
        service_path = '/etc/systemd/system/djangoApp_{}.service'.format(self.project_name)
        with open(service_path, 'w') as service:
            env_path = os.path.join(self.project_directory, 'venv', 'bin')
            content = '[Unit]\n' \
                      'Description=Gunicorn instance to serve Django App{project}\n' \
                      'After=network.target\n\n' \
                      '[Service]\n' \
                      'User={user}\n' \
                      'Group=www-data\n' \
                      'WorkingDirectory={wd}\n' \
                      'Environment="PATH={env}"\n' \
                      'ExecStart={env}/gunicorn --workers 2 --bind 127.0.0.1:8000 -m 007 {project}.wsgi:application\n\n' \
                      '[Install]\n' \
                      'WantedBy=multi-user.target\n' \
                      ''.format(project=self.project_name, wd=self.project_directory, env=env_path, user=getuser())
            service.write(content)
        print('> Project service created')
        with open(self.project_name + '-deployment.log', 'a') as dep_log:
            subprocess.run(['sudo', 'systemctl', 'start', 'djangoApp_{}.service'.format(self.project_name)],
                           stdout=dep_log, stderr=subprocess.STDOUT)
            subprocess.run(['sudo', 'systemctl', 'enable', 'djangoApp_{}.service'.format(self.project_name)],
                           stdout=dep_log, stderr=subprocess.STDOUT)
            subprocess.run(['sudo', 'systemctl', 'status', 'djangoApp_{}.service'.format(self.project_name)],
                           stdout=dep_log, stderr=subprocess.STDOUT)
        print('> System service djangoApp_{}.service started...'.format(self.project_name))

    def create_nginx_proxy(self):
        """
            Function to create nginx proxy
        :return:
        """
        print('Creating nginx configuration file for {}...'.format(self.project_name))
        config_path = '/etc/nginx/sites-available/djangoApp_{}'.format(self.project_name)
        domains = input('Enter the domain names (space separated) on which you have to host the Django app: ')
        with open(config_path, 'w') as config_file:
            content = 'server {{\n' \
                      '    listen      80;\n' \
                      '    server_name {domains};\n' \
                      "    location / {{\n" \
                      '        proxy_pass         "http://127.0.0.1:8000";\n' \
                      '        proxy_redirect     off;\n' \
                      '        proxy_set_header   Host $host;\n' \
                      '        proxy_set_header   X-Real-IP $remote_addr;\n' \
                      '        fastcgi_read_timeout 300s;\n' \
                      '        proxy_read_timeout 300;\n' \
                      '    }}\n' \
                      '    location = /favicon.ico {{ access_log off; log_not_found off; }}\n' \
                      '    location /static/ {{\n' \
                      '        root {project_dir};\n' \
                      '    }}' \
                      '    error_log  /var/log/nginx/djangoApp_{project}.log;\n' \
                      '    access_log /var/log/nginx/djangoApp_{project}_access.log;\n' \
                      '}}\n' \
                      ''.format(domains=domains, project=self.project_name, project_dir=self.project_directory)

            config_file.write(content)
        print('> NGINX config completed...')

        with open(self.project_name + '-deployment.log', 'a') as dep_log:
            subprocess.run(['sudo', 'ln', '-s', '/etc/nginx/sites-available/djangoApp_{}'.format(self.project_name),
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


def execute_django_deploy(project_details):
    """
        Function to execute Deploy sequence
    :return:
    """
    run = Deploy(project_details)
    print('> Starting deployment for {}...'.format(project_details['project_name']))
    run.initial_setup()
    run.create_gunicorn_process()
    run.create_nginx_proxy()
    run.complete_deploy_process()
