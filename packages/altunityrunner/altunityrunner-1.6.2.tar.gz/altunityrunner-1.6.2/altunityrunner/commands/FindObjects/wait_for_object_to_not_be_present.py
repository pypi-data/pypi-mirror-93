from altunityrunner.commands.command_returning_alt_elements import CommandReturningAltElements
from altunityrunner.altUnityExceptions import WaitTimeOutException
from altunityrunner.commands.FindObjects.find_object import FindObject
from loguru import logger
import time


class WaitForObjectToNotBePresent(CommandReturningAltElements):
    def __init__(self, socket, request_separator, request_end, by, value, camera_by, camera_path, timeout, interval, enabled):
        super(WaitForObjectToNotBePresent, self).__init__(
            socket, request_separator, request_end)
        self.by = by
        self.value = value
        self.camera_by = camera_by
        self.camera_path = camera_path
        self.timeout = timeout
        self.interval = interval
        self.enabled = enabled

    def execute(self):
        t = 0
        while (t <= self.timeout):
            try:
                logger.debug('Waiting for element ' +
                             self.value + ' to not be present...')
                FindObject(self.socket, self.request_separator, self.request_end,
                           self.by, self.value, self.camera_by, self.camera_path, self.enabled).execute()
                logger.debug("object found")
                time.sleep(self.interval)
                t += self.interval
            except Exception as ex:
                logger.debug(ex)
                break
        if t > self.timeout:
            logger.debug("WaitTimeOutException")
            raise WaitTimeOutException(
                'Element ' + self.value + ' still found after ' + str(self.timeout) + ' seconds')
        logger.debug("succcess")
