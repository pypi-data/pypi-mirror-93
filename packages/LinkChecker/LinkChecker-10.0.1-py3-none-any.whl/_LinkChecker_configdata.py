# -*- coding: iso-8859-1 -*-
# this file is automatically created by setup.py
install_purelib = '/'
install_platlib = '/LinkChecker-10.0.1.data/platlib'
install_lib = '/'
install_headers = '/LinkChecker-10.0.1.data/headers'
install_scripts = '/LinkChecker-10.0.1.data/scripts'
config_dir = '/LinkChecker-10.0.1.data/data/share/linkchecker'
install_data = '/LinkChecker-10.0.1.data/data'
name = 'LinkChecker'
version = '10.0.1'
author = 'LinkChecker Authors'
author_email = 'UNKNOWN'
maintainer = 'LinkChecker Authors'
maintainer_email = 'UNKNOWN'
url = 'https://linkchecker.github.io/linkchecker/'
license = 'GPL'
description = 'check links in web documents or full websites'
long_description = 'LinkChecker\n============\n\n|Build Status|_ |License|_\n\n.. |Build Status| image:: https://travis-ci.com/linkchecker/linkchecker.svg?branch=master\n.. _Build Status: https://travis-ci.com/linkchecker/linkchecker\n.. |License| image:: https://img.shields.io/badge/license-GPL2-d49a6a.svg\n.. _License: https://opensource.org/licenses/GPL-2.0\n\nCheck for broken links in web sites.\n\nFeatures\n---------\n\n- recursive and multithreaded checking and site crawling\n- output in colored or normal text, HTML, SQL, CSV, XML or a sitemap graph in different formats\n- HTTP/1.1, HTTPS, FTP, mailto:, news:, nntp:, Telnet and local file links support\n- restrict link checking with regular expression filters for URLs\n- proxy support\n- username/password authorization for HTTP, FTP and Telnet\n- honors robots.txt exclusion protocol\n- Cookie support\n- HTML5 support\n- a command line and web interface\n- various check plugins available, eg. HTML syntax and antivirus checks.\n\nInstallation\n-------------\n\nSee `doc/install.txt`_ in the source code archive for general information. Except the given information there, please take note of the following:\n\n.. _doc/install.txt: doc/install.txt\n\nPython 3.6 or later is needed.\n\nThe version in the pip repository may be old. Instead, you can use pip to install the latest code from git: ``pip3 install git+https://github.com/linkchecker/linkchecker.git``.\n\nUsage\n------\nExecute ``linkchecker https://www.example.com``.\nFor other options see ``linkchecker --help``.\n\nDocker usage\n-------------\n\n*The Docker images are out-of-date, pip installation is the only currently recommended method.*\n\nIf you do not want to install any additional libraries/dependencies you can use the Docker image.\n\nExample for external web site check::\n\n  docker run --rm -it -u $(id -u):$(id -g) linkchecker/linkchecker --verbose https://www.example.com\n\nLocal HTML file check::\n\n  docker run --rm -it -u $(id -u):$(id -g) -v "$PWD":/mnt linkchecker/linkchecker --verbose index.html\n'
keywords = ['link', 'url', 'site', 'checking', 'crawling', 'verification', 'validation']
platforms = ['UNKNOWN']
fullname = 'LinkChecker-10.0.1'
contact = 'LinkChecker Authors'
contact_email = 'UNKNOWN'
release_date = "29.1.2021"
portable = 0
