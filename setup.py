try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

from subprocess import Popen, PIPE

import boatd

version = Popen(['git', 'describe'],
                stdout=PIPE).communicate()[0].replace('v', '')
assert version.startswith(str(boatd.VERSION))

setup(
    name='boatd',
    version=version,
    author='Louis Taylor',
    author_email='kragniz@gmail.com',
    description=('Experimental daemon to control an autonomous sailing robot'),
    license='LGPL',
    keywords='boat sailing wrapper rest',
    url='https://github.com/boatd/boatd',
    packages=['boatd'],
    scripts=['boatd-start'],
    requires=['PyYAML'],
    install_requires=[
        'PyYAML >= 3.11'
        ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU Lesser General Public License v3 or later (LGPLv3+)',
        'Operating System :: POSIX :: Linux',
        'Topic :: Scientific/Engineering :: Interface Engine/Protocol Translator',
        'Topic :: Scientific/Engineering',
        'Topic :: Software Development :: Embedded Systems',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)
