try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

from subprocess import Popen, PIPE

setup(
    name='boatd',
    version='2.1.0',
    author='Louis Taylor',
    author_email='louis@kragniz.eu',
    description=('Experimental daemon to control an autonomous sailing robot'),
    license='LGPL',
    keywords='boat sailing wrapper rest',
    url='https://github.com/boatd/boatd',
    packages=['boatd'],
    scripts=['bin/boatd'],
    requires=[
        'PyYAML',
        'six'
        ],
    install_requires=[
        'PyYAML >= 3.11',
        'six'
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
