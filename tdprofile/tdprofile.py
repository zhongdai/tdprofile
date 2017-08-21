# coding=utf-8


"""
The main file for TDPROFILE
"""
import base64


class Profile(object):
    def __init__(self,username, url, password):
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
