from client.onem2m.OneM2MResource import OneM2MResource


# {
#     "sub": {
# 	"enc": {
# 		"net": [ ${NET} ],
# 		"ty": 4
# 	},
# 	"nct": ${NCT},
# 	"nu": ["${NU}"]	
#   }
# }
class Subscription(OneM2MResource):
    # Resource specific criteria.
    # @todo add remaining resource attribute from TS-0004 8.2.3
    M2M_ATTR_EVENT_NOTIFICATION_CRITERIA = 'm2m:enc'
    M2M_ATTR_NOTIFICATION_URI = 'nu'
    M2M_ATTR_NCT = 'nct'  # @note can not find in docs.

    def __init__(self, subscription):
        """
        """
        super().__init__('m2m:sub', subscription)        
