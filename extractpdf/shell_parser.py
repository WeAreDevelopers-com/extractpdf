"""This module includes a bunch of convenient base classes that are
reused in many of the other parser modules.
"""

import subprocess
import tempfile
import os
import errno

from . import exceptions
from .base_parser import BaseParser

class ShellParser(BaseParser):
    """The :class:`.ShellParser` extends the :class:`.BaseParser` to make
    it easy to run external programs from the command line with
    `Fabric <http://www.fabfile.org/>`_-like behavior.
    """

    @classmethod
    def run(cls, args):
        """Run ``command`` and return the subsequent ``stdout`` and ``stderr``
        as a tuple. If the command is not successful, this raises a
        :exc:`pdfextract.exceptions.ShellError`.
        """

        # run a subprocess and put the stdout and stderr on the pipe object
        try:
            pipe = subprocess.Popen(
                args, shell=True,
                stdout=subprocess.PIPE, stderr=subprocess.PIPE,
            )
        except OSError as e:
            if e.errno == errno.ENOENT:
                # File not found.
                # This is equivalent to getting exitcode 127 from sh
                raise exceptions.ShellError(
                    ' '.join(args), 127, '', '',
                )
            raise Exception(e)

        # pipe.wait() ends up hanging on large files. using
        # pipe.communicate appears to avoid this issue
        stdout, stderr = pipe.communicate()

        # if pipe is busted, raise an error (unlike Fabric)
        if pipe.returncode != 0:
            raise exceptions.ShellError(
                ' '.join(args), pipe.returncode, stdout, stderr,
            )

        return stdout, stderr

    @classmethod
    def temp_filename(cls):
        """Return a unique tempfile name.
        """
        # TODO: it would be nice to get this to behave more like a
        # context so we can make sure these temporary files are
        # removed, regardless of whether an error occurs or the
        # program is terminated.
        handle, filename = tempfile.mkstemp()
        os.close(handle)
        return filename