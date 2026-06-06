class PLCManager:

    def __init__(self):

        self.trigger = False

    def read_trigger(self):

        return self.trigger

    def set_trigger(
        self,
        state
    ):

        self.trigger = state

    def write_ok(self):
        print("PLC -> OK")

    def write_ng(self):
        print("PLC -> NG")