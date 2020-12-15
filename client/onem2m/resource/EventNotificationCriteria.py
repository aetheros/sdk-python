from client.onem2m.OneM2MResource import OneM2MResource, OneM2MResourceContent


class EventNotificationCriteria(OneM2MResource):
    def __init__(self, enc: OneM2MResourceContent):
        super().__init__('enc', enc)
