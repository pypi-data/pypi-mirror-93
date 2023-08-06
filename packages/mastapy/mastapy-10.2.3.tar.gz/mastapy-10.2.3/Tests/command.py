'''command.py

Module for running commands.

'''


import sys
import subprocess
from typing import Sequence


class CommandException(Exception):
    '''CommandException

    Exception raised from errors in running a command.

    '''


def run(*args: Sequence[str], bufsize: int = 1024 * 8):
    '''Runs a single command on the command line. Output is polled and written to stdout.

    Args:
        args (Sequence[str]): Sequence of arguments for the command line.
        bufsize (int, optional): Size of the buffer for the pipe.

    '''

    proc = subprocess.Popen(args, bufsize=bufsize, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

    try:
        out = proc.stdout.readline()
        while out and not proc.poll():
            sys.stdout.write(out.decode('utf-8'))
            out = proc.stdout.readline()
    except KeyboardInterrupt:
        sys.stdout.write('\n***Process terminated early by keyboard interrupt***\n')
        proc.terminate()
        proc.wait()
        raise CommandException('Command was interrupted.')
