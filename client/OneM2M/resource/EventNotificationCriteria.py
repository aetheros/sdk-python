from client.onem2m.OneM2MResource import OneM2MResource

class EventNotificationCriteria(OneM2MResource):
    def __init__(self, enc):
        self.__dict__ = enc

        self.short_name = 'enc'