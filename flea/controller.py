from  .modules.motor import drive, setup_motors


class Controller(object):
    def __init__(self, motors):
        self._motors = motors

    def run(self, command):
        # TODO: NOT IMPLEMENTED YET
        pass

    def _drive(self, data):
        # TODO: NOT IMPLEMENTED YET
        pass

    def _jump(self, data):
        # TODO: NOT IMPLEMENTED YET
        pass

    def _track(self, data):
        # TODO: NOT IMPLEMENTED YET
        pass
