class BaseNotification:
    TYPE = "base"

    def __init__(self, title, body, **kwargs):
        self.title = title
        self.body = body

    def send_push(self):
        self.devices.send_push(title=self.title, body=self.body, external_data=self.external_data)

    @property
    def devices(self):
        raise NotImplementedError

    @property
    def external_data(self):
        raise NotImplementedError
