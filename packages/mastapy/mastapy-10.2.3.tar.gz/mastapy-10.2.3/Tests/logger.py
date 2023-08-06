'''logger.py

Module for logging functionality.

'''


import sys


class Logger:
    '''Logger

    Custom logging class that prints to the console and to
    a file at the same time. Use this like a context
    manager.

    Args:
        file_path (str): Path to the output file.

    Example:

        >>> with Logger('path/to/my/file.txt'):
        ...     print('Hello world!')

    '''

    def __init__(self, file_path: str):
        self.file_path = file_path
        self.terminal = sys.stdout
        self.err = sys.stderr
        self.log = None


    def write(self, message: str):
        '''Implementing the stdout write interface.

        Args:
            message (str): Message to be written out.

        '''
        if self.log:
            self.terminal.write(message)
            self.log.write(message.replace('\r', ''))


    def flush(self):
        '''Implementing the stdout flush interface.'''

        if self.log:
            self.terminal.flush()
            self.log.flush()


    def __enter__(self):
        sys.stdout = self
        sys.stderr = self
        self.log = open(self.file_path, 'w')


    def __exit__(self, exception_type, exception_value, traceback):
        self.flush()

        self.log.close()
        self.log = None

        sys.stdout = self.terminal
        sys.stderr = self.err
