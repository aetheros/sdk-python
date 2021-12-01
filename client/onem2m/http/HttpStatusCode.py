# Copyright (c) Aetheros, Inc.  See COPYRIGHT

#!/usr/bin/env python


class HttpStatusCode:
    OK                    = 200
    CREATED               = 201
    ACCEPTED              = 202

    BAD_REQUEST           = 400
    FORBIDDEN             = 403
    NOT_FOUND             = 404
    METHOD_NOT_ALLOWED    = 405
    NOT_ACCEPTABLE        = 406
    REQUEST_TIMEOUT       = 408
    CONFLICT              = 409

    INTERNAL_SERVER_ERROR = 500
    NOT_IMPLEMENTED       = 501