from __future__ import absolute_import
import re
from xml.etree import ElementTree

def _tag(name):
    return '{http://fps.amazonaws.com/doc/2008-09-17/}%s' % name

NS_RE = re.compile(r'{([^}]*)}*')

class XmlObject(object):

    def __init__(self, xml):
        if isinstance(xml, (str, unicode)):
            self.xml = ElementTree.fromstring(xml)
        else:
            self.xml = xml
        self.parse()

    def tag(self, name, ns=None):
        if ns is None:
            match = NS_RE.match(self.xml.tag)
            if match:
                ns = match.groups()[0]
        if ns is None:
            return name
        else:
            return "{%s}%s" % (ns, name)

    def parse(self):
        pass

class ResponseError(XmlObject):

    @property
    def code(self):
        return self.xml.find(self.tag("Code")).text

    @property
    def message(self):
        return self.xml.find(self.tag("Message")).text

class ResponseMetadata(XmlObject):

    @property
    def requestId(self):
        return self.xml.find(self.tag("RequestId")).text

class Response(XmlObject):
    def parse(self):
        self.metadata = ResponseMetadata(self.xml.find(self.tag("ResponseMetadata")))

        self.errors = []
        errorsXml = self.xml.find(self.tag("Errors"))
        if errorsXml:
            for errorXml in errorsXml.findall(self.tag("Error")):
                self.errors.append(ResponseError(errorXml))

    def __repr__(self):
        return "<%s %r errors>" % (self.__class__.__name__, len(self.errors))

class PayResponse(Response):

    def __init__(self, xmlstring):
        super(PayResponse, self).__init__(xmlstring)

        pay_result = self.xml.find(self.tag('PayResult'))
        self.transactionId = pay_result.find(self.tag('TransactionId')).text
        self.transactionStatus = pay_result.find(self.tag('TransactionStatus')).text

    def __repr__(self):
        return "<%s transactionId=%r transactionStatus=%r>" % (self.__class__.__name__,
                                                               self.transactionId,
                                                               self.transactionStatus)
