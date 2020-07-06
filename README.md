# WebDeploy

A simple command line package for deploying Flask/Django apps on a Ubuntu system. <br>

## Install

### Using pip 

`$ sudo pip3 install webdeploy`

### Using source 

```
$ git clone https://github.com/idaljeetsingh/webdeploy
$ cd webdeploy
$ sudo python3 setup.py install
```

## Notes

* A fresh Ubuntu installation is preferred.
* ***Installing the package using sudo is necessary as it will make changes on system by installing packages to deploy the app.***


## Usage

Using the package is very simple. Just open the terminal and type respective command for either Flask or Django app.<br>
There are two ways for initiating the deploy sequence
1. From the project root directory - ***Picks up default information automatically***
2. Anywhere in the system - ***Requires to enter project information manually***

#### Flask

`WebDeploy-flask`

#### Django

`WebDeploy-django`

## License

[MIT License](LICENSE)