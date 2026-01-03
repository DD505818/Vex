class KillSwitch:
    def __init__(self):
        self.triggered = False

    def kill(self):
        self.triggered = True

    def resume(self):
        self.triggered = False
