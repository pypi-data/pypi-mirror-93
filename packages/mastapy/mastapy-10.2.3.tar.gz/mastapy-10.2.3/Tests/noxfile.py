'''noxfile.py

Defines all of the Nox sessions. This file is automatically ran when using the
command 'nox' in the same directory as this file.

Currently, we define sessions for all the supported versions of Python for
running tests on. We also run pylint and flake8 using the latest supported
version of Python.

'''


import os

import nox
from teamcity import is_running_under_teamcity


# Common constants
REQUIREMENTS_PATH = 'requirements.txt'
API_DIRECTORY = os.path.join('..', 'mastapy')
RESULTS_DIRECTORY = 'Results'
ENVS = {'TEAMCITY_VERSION': os.getenv('TEAMCITY_VERSION', default='')}
IS_TEAMCITY = is_running_under_teamcity()

# Supported versions of python. The last entry must be the most recent.
PYTHON_VERSIONS = ['3.5', '3.6', '3.7']

# pytest constants
PYTEST_DEFAULT_TEST_FILES = ['Tests']
PYTEST_FLAGS = []

# flake8 constants
FLAKE8_ERRORS_TO_IGNORE = ['E231', 'E501', 'E502', 'W291', 'W293',
                           'W391', 'F401', 'E128', 'E129', 'F403',
                           'F405', 'E743', 'E402']
FLAKE8_FLAGS = ['--statistics',
                f'--extend-ignore={",".join(FLAKE8_ERRORS_TO_IGNORE)}']

# update flags if teamcity is enabled
if IS_TEAMCITY:
    pylint_format = 'teamcity.pylint_reporter.TeamCityReporter'
    PYTEST_FLAGS.append('--teamcity')
    FLAKE8_FLAGS.append(f'--teamcity={IS_TEAMCITY}')


@nox.session(python=PYTHON_VERSIONS)
def pytest(session):
    '''Runs all tests over the mastapy package

    Note:
        This session is repeated for all specified Python versions.

        If you want to run specific tests:

        nox -- Tests/test.py

    '''

    session.install('-r', REQUIREMENTS_PATH)
    session.install('pytest')
    session.install('-e', '..')

    test_files = (
        session.posargs if session.posargs
        else PYTEST_DEFAULT_TEST_FILES)
    session.run('pytest', *test_files, *PYTEST_FLAGS, env=ENVS)


@nox.session(python=PYTHON_VERSIONS[-1])
def flake8(session):
    '''Linting tests for mastapy using the flake8 package

    Note:
        This session only runs with the latest specified version of Python

    '''

    session.install('-r', REQUIREMENTS_PATH)
    session.install('flake8')

    session.run('flake8', API_DIRECTORY, *FLAKE8_FLAGS, env=ENVS)
