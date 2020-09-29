from client.OneM2M.OneM2MResource import OneM2MResource


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
    M2M_ATTR_EVENT_NOTIFICATION_CRITERIA = 'enc'
    M2M_ATTR_NOTIFICATION_URI = 'nu'
    M2M_ATTR_NCT = 'nct' # @note can not find in docs.

    def __init__(self, subscription):
        """
        """
        self.__dict__ = subscription 

        # Resource short name.
        OneM2MResource.short_name = 'sub'

