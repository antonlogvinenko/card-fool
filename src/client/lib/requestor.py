'''Containts defenition of Requestor class used for sending requests to the server.
'''

import httplib
import urllib
import time

class Requestor:
    def __init__(self, host='', script=''):
        '''Initialization. Takes host name and script path.
        '''
        self._headers = {"Content-type": "application/x-www-form-urlencoded",
                        "Accept": "text/plain",
                        "Cache-Control": "no-store, no-cache, must-revalidate",
                        }
        self._host = host
        self._script = script
    def set_host(self, host):
        '''Change host.
        '''
        self._host = host
    def get_host(self):
        '''Get host name value.
        '''
        return self._host
    def get_script(self):
        '''Get script path.
        '''
        return self._script
    def set_script(self, script):
        '''Change script value.
        '''
        self._script = script
    def get_headers(self):
        '''Get current headers value.
        '''
        return self._headers
    def make_request(self, command):
        '''Send a request to 'self._script'
        script on 'self._host' host.  
        '''
        conn = httplib.HTTPConnection(self.get_host())
        conn.request("POST", self.get_script(), command, self.get_headers())
        #conn.request("GET", self.get_script() + '?' + command)
        response = conn.getresponse()
        data = response.read().replace('\r\n', '\n')
        conn.close()
        return data