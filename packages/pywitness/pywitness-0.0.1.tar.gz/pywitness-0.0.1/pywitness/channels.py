from abc import abstractmethod


class Channel:
    @abstractmethod
    def emit(self, key, value, timestamp):
        pass


class ConsoleChannel(Channel):
    def emit(self, key, value, timestamp):
        print(f'{key}:{value} (@ {timestamp})')


class PywitnessChannel(Channel):
    def __init__(self, api_url, api_key=None):
        self.api_url = api_url
        self._api_key = None
        self.api_key = api_key

    @property
    def api_key(self):
        return self._api_key

    @api_key.setter
    def api_key(self, value):
        # test api_key before setting
        self._api_key = value

    def emit(self, key, value, timestamp):
        pass
