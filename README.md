# WebDeploy

A simple command line package for deploying Flask/Django apps on a Ubuntu system. <br>

[![made-with-python](https://img.shields.io/badge/Made%20with-Python-1f425f.svg)](https://www.python.org/)
[![Downloads](https://pepy.tech/badge/webdeploy)](https://pepy.tech/project/webdeploy)
[![PyPI version shields.io](https://img.shields.io/pypi/v/WebDeploy.svg)](https://pypi.python.org/pypi/WebDeploy/)
[![GitHub issues](https://img.shields.io/github/issues/idaljeetsingh/WebDeploy.svg)](https://GitHub.com/idaljeetsingh/WebDeploy/issues/)
[![PyPI license](https://img.shields.io/pypi/l/WebDeploy.svg)](https://pypi.python.org/pypi/WebDeploy/)


## Changelog <samp>v1.1.0</samp> 📣

⚡ Added support for MongoDB 


## Install ⌨️

### Using pip 

`$ sudo pip3 install webdeploy`

### Using source 

```
$ git clone https://github.com/idaljeetsingh/webdeploy
$ cd webdeploy
$ sudo python3 setup.py install
```

## Notes 📝

* A fresh Ubuntu installation is preferred.
* ***Installing the package using sudo is necessary as it will make changes on system by installing packages to deploy the app.***


## Databases Supported 🦾 

* MongoDB

## Usage ⚙️

Using the package is very simple. Just open the terminal and type respective command for either Flask or Django app.<br>
There are two ways for initiating the deploy sequence
1. From the project root directory - ***Picks up default information automatically***
2. Anywhere in the system - ***Requires to enter project information manually***

#### Flask

`WebDeploy-flask`

#### Django

`WebDeploy-django`

## Tutorials 📚

Flask: <a href="https://medium.com/@idaljeetsingh/deploying-flask-app-on-ubuntu-using-webdeploy-eb41aa44ea76?source=---------2------------------">Deploying Flask App on Ubuntu using WebDeploy</a>

Django: <a href="https://medium.com/@idaljeetsingh/deploying-django-app-on-ubuntu-using-webdeploy-fda44bba620a">Deploying Django App on Ubuntu using WebDeploy</a>

## License 📜

[MIT License](LICENSE) © [Daljeet Singh Chhabra](https://GitHub.com/iDaljeetSingh)


[![ForTheBadge built-with-love](http://ForTheBadge.com/images/badges/built-with-love.svg)](https://GitHub.com/Naereen/)
