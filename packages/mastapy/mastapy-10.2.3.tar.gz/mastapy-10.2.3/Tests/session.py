'''session.py

Module for session functionality.

'''


_SESSIONS = dict()


class SessionException(Exception):
    '''SessionException

    Exception raised when a session fails.

    '''


def session(name: str):
    '''Decorator method for labelling sessions in the run module.

    Args:
        name (str): The name of the session

    Returns:
        the decorated function

    '''

    def _session(func):
        _SESSIONS[name] = func
        return func

    return _session


def run_session(name: str, time_marker: str):
    '''Runs a single session.

    Args:
        name (str): The name of the session
        time_marker (str): Time marker for the report

    '''

    try:
        _SESSIONS[name](time_marker)
    except KeyError:
        raise SessionException(f'Failed to find session \'{name}\'')


def run_all_sessions(time_marker: str):
    '''Runs all defined sessions.

    Args:
        time_marker (str): Time marker for the report

    '''

    for sess in _SESSIONS.values():
        sess(time_marker)
