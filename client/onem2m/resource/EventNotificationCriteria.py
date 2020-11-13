from client.onem2m.OneM2MResource import OneM2MResource


class EventNotificationCriteria(OneM2MResource):
    def __init__(self, enc):
        super().__init__('m2m:enc', enc)        
