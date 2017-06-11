try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

from subprocess import Popen, PIPE

setup(
    name='boatd',
    version='3.2.0',
    author='Louis Taylor',
    author_email='louis@kragniz.eu',
    description=('Experimental daemon to control an autonomous sailing robot'),
    license='LGPL',
    keywords='boat sailing wrapper rest',
    url='https://github.com/boatd/boatd',
    package_dir = {
        'boatd': 'boatd',
        'boatd.coreplugins': 'boatd/coreplugins',
        'boatd.coreplugins.mavlink_common': 'boatd/coreplugins/mavlink_common',
    },
    packages=['boatd', 'boatd.coreplugins', 'boatd.coreplugins.mavlink_common'],
    scripts=['bin/boatd'],
    install_requires=[
        'PyYAML',
        'six',
        'pyserial',
        'tornado',
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
