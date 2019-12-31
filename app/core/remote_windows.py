import winrm
import os
from app.core.logger import logger


class RemoteSession:
    def __init__(self, server, auth):
        self._server = server
        self._auth = auth

    @property
    def _session(self):
        return winrm.Session(self._server, self._auth, transport='credssp')

    def run_cmd(self, command):
        logger.info(f'running {command} against {self._server}')
        result = self._session.run_cmd(command)
        if result.std_err:
            logger.error(f'Error running {command} against {self._server}: {result.std_err.decode("utf-8")}')
        return result

    def ls(self, directory=''):
        """Runs the equivalent ls or dir for a remote connection for the given directory."""
        cmd = f'DIR {directory} /B'
        result = self.run_cmd(cmd)
        return split_files(result.std_out.decode('utf-8'))

    def copy(self, source_file, destination):
        """Copies the given target file to the given target file/directory"""
        if not self._check_file_exists(destination, source_file):
            cmd = f'COPY {source_file} {destination}'
            result = self.run_cmd(cmd)
            return result.status_code
        else:
            logger.info(f'File {source_file} already exists in {destination} and was not copied')

    def delete_file(self, file):
        """Deletes the given target file."""
        cmd = f'DEL /f {file}'
        result = self.run_cmd(cmd)
        return result.status_code

    def _check_file_exists(self, destination, source_file):
        file_name = os.path.basename(source_file)
        target_file = os.path.join(destination, file_name)
        cmd = f'dir {target_file}'
        result = self.run_cmd(cmd)
        return 'File Not Found' not in result.std_err.decode("utf-8")


def split_files(file_string):
    """
    Converts the given string to a sequence of files.
    Ignore the last item as this will be a blank string.
    """
    return file_string.split('\r\n')[:-1]
