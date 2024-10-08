#!/usr/bin/env python
from __future__ import absolute_import
from __future__ import print_function

import os
import sys
import subprocess
import re

from setuptools import setup
from setuptools.command.sdist import sdist as _sdist
from setuptools.command.install import install as _install

VERSION_PY = """
# This file is originally generated from Git information by running 'setup.py
# version'. Distribution tarballs contain a pre-generated copy of this file.
__version__ = '%s'
"""


def update_version_py():
    if not os.path.isdir(".git"):
        print("This does not appear to be a Git repository.")
        return
    try:
        #p = subprocess.Popen(["git", "describe","--tags", "--always"],
        #        stdout=subprocess.PIPE)
        p = subprocess.Popen("git rev-list HEAD --count".split(),
                stdout=subprocess.PIPE)


    except EnvironmentError:
        print("unable to run git, leaving lmz/__version__.py alone")
        return
    stdout = p.communicate()[0].decode("utf-8")

    print ("stdout:",stdout)
    if p.returncode != 0:
        print("unable to run git, leaving lmz/__version__.py alone")
        return
    ver = "0.1."+stdout.strip()
    #ver = str(int(ver,16)) # pypi doesnt like base 16
    f = open("lmz/__version__.py", "w")
    f.write(VERSION_PY % ver)
    f.close()
    print("set lmz/__version__.py to '%s'" % ver)


def get_version():
    try:
        f = open("lmz/__version__.py")
    except EnvironmentError:
        return None
    for line in f.readlines():
        mo = re.match("__version__ = '([^']+)'", line)
        if mo:
            ver = mo.group(1)
            return ver
    return None


class sdist(_sdist):

    def run(self):
        update_version_py()
        self.distribution.metadata.version = get_version()
        return _sdist.run(self)


class install(_install):

    def run(self):
        _install.run(self)

    def checkProgramIsInstalled(self, program, args, where_to_download,
                                affected_tools):
        try:
            subprocess.Popen([program, args], stderr=subprocess.PIPE, stdout=subprocess.PIPE)
            return True
        except EnvironmentError:
            # handle file not found error.
            # the config file is installed in:
            msg = "\n**{0} not found. This " \
                  "program is needed for the following "\
                  "tools to work properly:\n"\
                  " {1}\n"\
                  "{0} can be downloaded from here:\n " \
                  " {2}\n".format(program, affected_tools,
                                  where_to_download)
            sys.stderr.write(msg)

        except Exception as e:
            sys.stderr.write("Error: {}".format(e))

setup(
    name='lmz',
    version=get_version(),
    author='Stefan Mautner',
    author_email='myl4stn4m3stef@gmail.com',
    packages=['lmz'],
    python_requires='>=3.8',
    include_package_data=True,
    package_data={},
    url='https://github.com/smautner/listmapzip',
    license='GPLv3',
    description='small functions that should be part of python3, supplementing generator functions',
    long_description=open('README.md').read(),
    long_description_content_type = 'text/markdown',
    install_requires=[],
    cmdclass={'sdist': sdist, 'install': install}
)
