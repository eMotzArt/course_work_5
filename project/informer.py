from .utils import singleton


@singleton
class Informer:
    def __init__(self):
        self.messages: list[str] = []

    def add_note(self, msg: str):
        self.messages.append(msg)

    def clear(self):
        self.messages.clear()

    def get_message(self):
        message = '\n'.join(self.messages)
        self.clear()
        return message
