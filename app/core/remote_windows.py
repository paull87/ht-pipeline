import winrm


class RemoteWindow:
    def __init__(self, server, auth):
        self._server = server
        self._auth = auth

    @property
    def _session(self):
        return winrm.Session(self._server, self._auth, transport='ntlm')

    def run_cmd(self, command):
        return self._session.run_cmd(command)

    def ls(self, directory=''):
        """Runs the equivalent ls or dir for a remote connection for the given directory."""
        result = self.run_cmd(f'DIR {directory} /B')
        print(f'DIR {directory} /B')
        print(f'std_err: {result.std_err.decode("utf-8")}')
        return split_files(result.std_out.decode('utf-8'))

    def copy(self, target, destination):
        """Copies the given target file to the given target file/directory"""
        result = self.run_cmd(f'COPY {target} {destination}')
        print(f'COPY {target} {destination}')
        print(f'std_err: {result.std_err.decode("utf-8")}')
        return result.status_code


def split_files(file_string):
    """
    Converts the given string to a sequence of files.
    Ignore the last item as this will be a blank string.
    """
    return file_string.split('\r\n')[:-1]
