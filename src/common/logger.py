import time
import os

class Logger:
    def __init__(self):
        dir = "..\\..\\messages\\" + str(time.strftime("%m_%d_%H")) + "\\"
        try: os.mkdir(dir)
        except OSError: pass
        self._filename =  dir + "client_" + str(time.strftime("%M%S")) + ".log"
        self._file = open(self._filename, 'w+')
    def received(self, txt):
        '''Log received command.
        '''
        self._file.write(txt + "\n\n")
    def sent(self, txt):
        '''Log sent command.
        '''
        self._file.write(txt + "\n")