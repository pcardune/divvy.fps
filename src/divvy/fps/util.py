########################################################################
# Copyright (c) 2009 Paul Carduner and Contributors
# All Rights Reserved
# This file is part of divvy.fps.
#
# divvy.fps is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# divvy.fps is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with divvy.fps.  If not, see
# <http://www.gnu.org/licenses/>.
#########################################################################

import urllib
import hmac
import sha
import base64

def query_string(parameters):
    return "?"+urllib.urlencode(sorted([item for item in parameters.items()
                                        if item[1] is not None]))

def get_signature(key, parameters):
    """Get a signature for FPS requests.

    Given a set of query parameters as a dict, this will compute a
    signature for use with amazon FPS as documented here:

    http://docs.amazonwebservices.com/AmazonFPS/2008-09-17/FPSAdvancedGuide/index.html?APPNDX_GeneratingaSignature.html

    """
    msg = "".join(("%s%s" % item
                   for item in sorted(parameters.items(), key=lambda item: item[0].lower())
                   if item[1] is not None))
    return base64.encodestring(hmac.new(key, msg, sha).digest()).strip()
