import logging
import os
import subprocess
import threading


log = logging.getLogger(__name__)


class LogPipe(threading.Thread):
    def __init__(self, level, name):
        threading.Thread.__init__(self)
        self.name = name
        self.daemon = True
        self.level = level
        self.fd_read, self.fd_write = os.pipe()
        self.pipe_reader = os.fdopen(self.fd_read)
        self.start()

    def fileno(self):
        return self.fd_write

    def run(self):
        for line in iter(self.pipe_reader.readline, ''):
            logging.log(self.level, self.name + ': ' + line.strip('\n'))

        self.pipe_reader.close()

    def close(self):
        os.close(self.fd_write)


class Behaviour(object):
    def __init__(self, name, filename):
        self.name = name
        self.filename = filename
        self.running = False
        self.process = None
        self.logpipe = None

    def start(self):
        self.logpipe = LogPipe(logging.INFO, self.name)
        self.process = subprocess.Popen([self.filename],
                                        stdout=self.logpipe,
                                        stderr=self.logpipe)
        self.running = True

    def end(self):
        '''
        Send a SIGTERM signal (15) to the behaviour script to nicely ask it to
        stop.
        '''
        if self.running:
            self.process.terminate()
            self.process.wait()
            self.running = False
            self.logpipe.close()
