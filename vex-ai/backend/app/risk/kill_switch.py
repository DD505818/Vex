class KillSwitch:
    def __init__(self):
        self.triggered = False

    def kill(self):
        self.triggered = True

    def resume(self):
        self.triggered = False


_shared_kill_switch = KillSwitch()


def get_kill_switch() -> KillSwitch:
    return _shared_kill_switch
