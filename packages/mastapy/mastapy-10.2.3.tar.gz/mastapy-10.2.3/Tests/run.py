'''run.py

Main module for running the tests. Unlike running nox directly,
this module creates reports for each test. This module should be
used by the build agents for testing.

Usage:

    To run all of the tests, simply call:

        >>> python run.py

    To run a specific session, call:

        >>> python run.py --session <SESSION_NAME>

'''


import datetime
import os
import argparse as ap
from typing import Tuple

import command
import session
from logger import Logger


RESULTS_DIRECTORY = 'Results'
PYTEST_OUTPUT_PATH = os.path.join(RESULTS_DIRECTORY, 'pytest')
FLAKE8_OUTPUT_PATH = os.path.join(RESULTS_DIRECTORY, 'flake8')

DESC = 'Runs all of the tests and generates reports based on the tests.'


def test_logging_setup():
    '''Setup before a session is run.

    Note:
        This is a basic setup check to make sure the Results folder has been
        created.

    '''

    if not os.path.isdir(RESULTS_DIRECTORY):
        os.mkdir(RESULTS_DIRECTORY)


def get_time_marker() -> str:
    '''Returns a time marker for labeling results files with.

    Returns:
        str

    Note:
        The time marker is used to make sure the result file names are unique,
        but also so you know when the particular test was run.

    '''

    now = datetime.datetime.now()
    macro = f'{now.year}-{now.month}-{now.day}'
    micro = f'{now.hour}-{now.minute}-{now.second}-{now.microsecond}'
    return f'--{macro}--{micro}'


def get_file_names(file_name: str) -> Tuple[str, str]:
    '''Returns filenames for .txt and .json files.

    Args:
        file_name (str): File name

    Returns:
        Tuple[str, str]: First value is .txt file name, second is .json

    '''

    return file_name + '.txt', file_name + '.json'


@session.session('pytest')
def run_pytest(time_marker: str):
    '''Running the pytest session.

    Args:
        time_marker (str): Time marker for the report

    '''

    report_name = PYTEST_OUTPUT_PATH + time_marker
    report_file, report_json = get_file_names(report_name)

    with Logger(report_file):
        command.run('py', '-m', 'nox', '-s', 'pytest', '--report', report_json)


@session.session('flake8')
def run_flake8(time_marker: str):
    '''Running the flake8 session.

    Args:
        time_marker (str): Time marker for the report

    '''

    report_name = FLAKE8_OUTPUT_PATH + time_marker
    report_file, report_json = get_file_names(report_name)

    with Logger(report_file):
        command.run('py', '-m', 'nox', '-s', 'flake8', '--report', report_json)


def parse_args():
    '''Parses command line arguments.'''

    parser = ap.ArgumentParser(description=DESC)
    parser.add_argument('-s', '--session', type=str,
                        help='The session to run. Leave empty to run all.')

    args = parser.parse_args()
    return args.session


def main():
    '''Main entry point for the module.'''

    session_name = parse_args()
    test_logging_setup()
    time_marker = get_time_marker()

    if session_name:
        session.run_session(session_name, time_marker)
    else:
        session.run_all_sessions(time_marker)


if __name__ == '__main__':
    main()
