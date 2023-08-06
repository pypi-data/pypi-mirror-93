import logging
import os

class CleanLogger:

    def __init__(
        self, 
        name, 
        streamhandler_level = logging.INFO,
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    ):
        log = logging.getLogger(name)
        log.setLevel(logging.DEBUG)

        ch = logging.StreamHandler()
        ch.setLevel(streamhandler_level)
        ch.setFormatter(formatter)

        log.addHandler(ch)

        self._log = log
        self._formatter = formatter
        self._fileloggers = {}

    def log(self):
        return self._log

    def debug(self, msg):
        self._log.debug(msg)

    def info(self, msg):
        self._log.info(msg)

    def warning(self, msg):
        self._log.warning(msg)

    def error(self, msg):
        self._log.error(msg)

    def critical(self, msg):
        self._log.critical(msg)

    def add_filelogger(self, filename, loglevel = logging.DEBUG, append = False):
        self._log.info("Registering log file '{}' ...".format(filename))
        folder = os.path.dirname(filename)
        if folder and not os.path.exists(folder):
            self._log.debug("Creating directory '{}' ...".format(folder))
            try:
                os.makedirs(folder)
            except:
                self._log.error("Cannot create folder '{fol}'. I skip adding a log file {f}.".format(fol=folder, f=filename))
                return

        fh = logging.FileHandler(filename, mode='a' if append else 'w')
        fh.setLevel(loglevel)
        fh.setFormatter(self._formatter)

        self._log.addHandler(fh)
        self._fileloggers[filename] = fh

    def remove_filelogger(self, filename):
        self._log.info("Unregistering log file '{}' ...".format(filename))
        if not filename in self._fileloggers.keys():
            self._log.info("Log file '{}' is not registered. I skip this.".format(filename))
            return

        self._log.removeHandler(self._fileloggers[filename])
        del(self._fileloggers[filename])

