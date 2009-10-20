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
