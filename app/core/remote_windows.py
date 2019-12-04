import winrm
from app.core.logging import logger


class RemoteWindow:
    def __init__(self, server, auth):
        self._server = server
        self._auth = auth

    @property
    def _session(self):
        return winrm.Session(self._server, self._auth, transport='credssp')

    def run_cmd(self, command):
        return self._session.run_cmd(command)

    def ls(self, directory=''):
        """Runs the equivalent ls or dir for a remote connection for the given directory."""
        cmd = f'DIR {directory} /B'
        logger.info(f'running {cmd} against {self._server}')
        result = self.run_cmd(f'DIR {directory} /B')
        if result.std_err:
            logger.error(f'Error running {cmd} against {self._server}: {result.std_err.decode("utf-8")}')
        return split_files(result.std_out.decode('utf-8'))

    def copy(self, target, destination):
        """Copies the given target file to the given target file/directory"""
        result = self.run_cmd(f'COPY {target} {destination}')
        return result.status_code


def split_files(file_string):
    """
    Converts the given string to a sequence of files.
    Ignore the last item as this will be a blank string.
    """
    return file_string.split('\r\n')[:-1]
