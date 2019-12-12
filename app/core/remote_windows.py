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

    def copy(self, target, destination):
        """Copies the given target file to the given target file/directory"""
        if not self._check_file_changed(destination, target):
            cmd = f'COPY {target} {destination}'
            result = self.run_cmd(cmd)
            return result.status_code
        else:
            logger.info(f'File {destination} already exists and was not copied')

    def delete_file(self, file):
        """Deletes the given target file."""
        cmd = f'DEL /f {file}'
        result = self.run_cmd(cmd)
        return result.status_code

    def file_modified_date(self, file):
        """Returns the modified date of a file."""
        return False
        # TODO: forfiles doesn't support UNC so have to find another way to get file date.
        directory, file_name = os.path.split(file)
        cmd = f'forfiles /P {directory} /M {file_name} /C "cmd /c echo @FDATE @FTIME"'
        result = self.run_cmd(cmd)
        return result.std_out.decode('utf-8').strip()

    def _check_file_changed(self, destination, target):
        file_name = os.path.basename(destination)
        target_file = os.path.join(target, file_name)
        return self.file_modified_date(destination) == self.file_modified_date(target_file)


def split_files(file_string):
    """
    Converts the given string to a sequence of files.
    Ignore the last item as this will be a blank string.
    """
    return file_string.split('\r\n')[:-1]
