from client.onem2m.OneM2MResource import OneM2MResource


class EventNotificationCriteria(OneM2MResource):
    def __init__(self, enc: OneM2MResource.Content):
        super().__init__('enc', enc)
