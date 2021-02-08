from my_io.streams import BasicStream
from ui.abstract_ui import AbstractUI


class BasicUI(AbstractUI):
    stream = BasicStream()
