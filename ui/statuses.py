class Statuses:
    OK = "OK"
    FAIL = "FAIL"

class Status:
    _status = Statuses.OK

    def __init__(self, status_name: str = None):
        if not status_name:
            self.set(status_name)

    def __eq__(self, other: "Status"):
        return self._status == other._status

    def set(self, value: str):
        self._status = value
