# coding=utf-8


"""
The main file for TDPROFILE
"""
import base64
import os
import sys

class ProfileCollection(object):
    """Represent all profiles as a collection

    """
    JSON_FILE = 'tdprofile.json'
    def __init__(self):
        best_path = self._find_best_path()
        if best_path is None:
            raise ValueError('Could not find the best path to save data!')

        self._json_path = os.path.join(best_path, self.JSON_FILE)
        if not os.path.isfile(self._json_path):
            self._profiles = []
        else:
            self._profiles = self._load_profile()

    def __str__(self):
        return '<ProfileCollection>'

    def __setitem__(self, key, value):
        if not isinstance(value, Profile):
            raise TypeError('The value must be a `Profile` type')
        self._profile[key] = value
        
    def _save_profile(self):
        pass

    def _find_best_path(self):
        """Find the best possible path to save the josn file

        The order of path is,
        1 - check the TDPROFILE_PATH Environment Variable
        2 - use Windows %APPDATA%
        3 -
        Args:
            None
        """
        path1 = sys.environ.get('TDPROFILE_PATH',None)
        path2 = sys.environ.get('APPDATA',None)
        return  path1 or path2


class Profile(object):
    """Represent the Teradata connection profile, username, url and password

    Attributes:
        password (str): the readable password
    """
    def __init__(self,label, username, url, password):
        """The init function of Profile

        Args:
            label (str): The name of connection, eg. TDP1, TDP3 or TDP5
            username (str): The salary number, starts with `M`,`F` or `L`
            url (str): The database url
            password (str): The password of Teradata user

        """
        if not isinstance(username, str) or \
           not isinstance(url, str) or \
           not isinstance(password, str):
           raise TypeError('Please make sure username, url, and password are string')


        self._username = username
        self._url = url


        self._password = base64.b64encode(b'{}'.format(password))

    def __str__(self):
        return 'Profile <{u}@{url}>'.format(u=self._username, url=self._url)

    def __repr__(self):
        return self.__str__

    @property
    def password(self):
        return base64.b64decode(self._password).decode('utf-8')



def command_line_runner():
    print('Hello TDPROFILE')
