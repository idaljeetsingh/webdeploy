"""
    File            :   setup.py
    Author          :   Daljeet Singh Chhabra
    Date Created    :   03-07-2020
    Date Modified   :   04-09-2020
"""
import setuptools

with open('README.md') as f:
    README = f.read()

setuptools.setup(
    author="Daljeet Singh Chhabra",
    author_email="idaljeetsingh@outlook.com",
    name='WebDeploy',
    license="MIT",
    description='WebDeploy is a python package for deploying Flask/Django applications at ease.',
    version='v1.1.0',
    long_description=README,
    long_description_content_type='text/markdown',
    entry_points={
        'console_scripts': [
            'WebDeploy-flask=WebDeploy.scripts.runner:deploy_flask',
            'WebDeploy-django=WebDeploy.scripts.runner:deploy_django',
        ],
    },
    url='https://github.com/idaljeetsingh/WebDeploy',
    packages=setuptools.find_packages(),
    python_requires=">=3.5",
    install_requires=[''],
    classifiers=[
        # Trove classifiers
        # (https://pypi.python.org/pypi?%3Aaction=list_classifiers)
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Topic :: Software Development :: Libraries',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Internet :: WWW/HTTP :: HTTP Servers',
    ],
)
