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

import time
import logging
import urllib2
import decimal
import datetime

from divvy.fps import base
from divvy.fps import util
from divvy.fps import conf
from divvy.fps import xml

LOGGER = logging.getLogger('divvy.fps.api')
SANDBOX_ENDPOINT = 'https://fps.sandbox.amazonaws.com'
ENDPOINT = 'https://fps.amazonaws.com'

TIME_FORMAT = "%Y-%m-%dT%H:%M:%SZ"
AMAZON_FPS_API_VERSION = '2008-09-17'

class ApiClient(base.AmazonFPSClient):
    """Client for accessing the FPS REST api."""

    def __init__(self,access_key_id=None,secret_key=None,endpoint=None):
        super(ApiClient, self).__init__(access_key_id=access_key_id, secret_key=secret_key)

        if endpoint is None:
            endpoint = SANDBOX_ENDPOINT if conf.RUN_IN_SANDBOX else ENDPOINT
        self.endpoint = endpoint

    def get_query_string(self, parameters):
        """Return a query string for the given keyword arguments.

        This will include the correct calleryKey, version, and
        generated query signature needed by amazon.
        """
        parameters.setdefault('AWSAccessKeyId', self.access_key_id)
        parameters.setdefault('Version', AMAZON_FPS_API_VERSION)
        parameters['SignatureVersion'] = '1'
        parameters['Signature'] = util.get_signature(self.secret_key, parameters)
        return util.query_string(parameters)

    def call(self, url):
        data = None
        success = False
        LOGGER.info("Making call to AWS FPS: %s", url)
        try:
            response = urllib2.urlopen(url)
        except urllib2.HTTPError, e:
            data = e.read()
            LOGGER.warn("Got an HTTP error retrieving %r: %s", url, data)
            e.close()
        else:
            data = response.read()
            LOGGER.debug("Successfully retrieved %r.  Got %r", url, data)
            response.close()
            success = True
        return data, success

    def pay(self, callerReference, senderTokenId, transactionAmount):
        LOGGER.info("Initiating pay request for callerReference %r", callerReference)
        timestamp = time.strftime(TIME_FORMAT, time.gmtime())
        qs = self.get_query_string({
                'Action':'Pay',
                'Timestamp':timestamp,
                'CallerReference':callerReference,
                'TransactionAmount.Value':transactionAmount,
                'TransactionAmount.CurrencyCode':'USD',
                'SenderTokenId':senderTokenId})
        url = self.endpoint+'/'+qs

        data, success = self.call(url)
        if success:
            response = xml.PayResponse(data)
        else:
            response = xml.Response(data)

        LOGGER.info("Got pay response: %r", response)
        return response

class Enum(object):

    def __init__(self, **kwargs):
        self.__items = kwargs
        for k, v in self.__items.items():
            setattr(self, k, v)

    def __contains__(self, name):
        return name in self.__items.values()


IPNTransactionStatusCodes = Enum(
    CANCELLED = 'CANCELLED',
    FAILURE = 'FAILURE',
    PENDING = 'PENDING',
    RESERVED = 'RESERVED',
    SUCCESS = 'SUCCESS',
    )


class IPNResponse(base.ParameterizedResponse):

    def __repr__(self):
        return "<%s parameters=%r>" % (self.__class__.__name__, self.parameters)

    @property
    def address_full_name(self):
        """Full name of the buyer/sender."""
        return self.parameters.get('addressFullName')

    @property
    def address_line1(self):
        """Sender's address (first line). For IPN, this element is
        returned only if the value has been updated with Amazon."""
        return self.parameters.get('addressLine1')

    @property
    def address_line2(self):
        """Sender's address (second line). For IPN, this element is
        returned only if the value has been updated with Amazon."""
        return self.parameters.get('addressLine2')

    @property
    def address_state(self):
        """Sender's state. For IPN, this element is returned only if
        the value has been updated with Amazon."""
        return self.parameters.get('addressState')

    @property
    def address_zip(self):
        """Sender's post code. For IPN, this element is returned only
        if the value has been updated with Amazon."""
        return self.parameters.get('addressZip')

    @property
    def address_country(self):
        """Sender's country. For IPN, this element is returned only if
        the value has been updated with Amazon."""
        return self.parameters.get('addressCountry')

    @property
    def address_phone(self):
        """Sender's phone number. For IPN, this element is returned
        only if the value has been updated with Amazon."""
        return self.parameters.get('addressPhone')

    @property
    def buyer_email(self):
        """Sender's e-mail address."""
        return self.parameters.get('buyerEmail')

    @property
    def buyer_name(self):
        """Sender's name."""
        return self.parameters.get('buyerName')

    @property
    def custom_data(self):
        """Data passed by the customer in the Pay call is returned in
        this element."""
        return self.parameters.get('customData')

    @property
    def customer_email(self):
        """Customer's e-mail address."""
        return self.parameters.get('customerEmail')

    @property
    def customer_name(self):
        """Buyer/Sender Full Name."""
        return self.parameters.get('customerName')

    @property
    def date_installed(self):
        """If the notificationType element (below) is
        TokenCancellation, this element contains the date the token
        was installed."""
        return self.parameters.get('dateInstalled')

    @property
    def integrator_id(self):
        """If present, this is the id of the solution provider
        assisting with the transaction."""
        return self.parameters.get('integratorId')

    @property
    def is_shipping_address_provided(self):
        """If the IPN results include address updates, this element
        contains TRUE. Otherwise this element is not present in the
        response."""
        return self.parameters.get('isShippingAddressProvided') is not None

    @property
    def operation(self):
        """The payment operation for this transaction."""
        return self.parameters.get('operation')

    @property
    def notification_type(self):
        """Notification type may be either TokenCancellation or TransactionStatus"""
        notification_type = self.parameters.get('notificationType')
        if notification_type not in ('TokenCancellation', 'TransactionStatus'):
            LOGGER.error("Got invalid ipn notification type: %r", notification_type)
        return notification_type

    @property
    def payment_method(self):
        """The payment method used by the sender."""
        return self.parameters.get('paymentMethod')

    @property
    def payment_reason(self):
        """Reason for payment."""
        return self.parameters.get('paymentReason')

    @property
    def recipient_email(self):
        """Recipient's e-mail address."""
        return self.parameters.get('recipientEmail')

    @property
    def recipient_name(self):
        """Recipient's name."""
        return self.parameters.get('recipientName')

    @property
    def signature(self):
        """The encoded string the caller uses to verify the
        IPN. Amazon Payments calculates the signature using the
        elements in the returnURL. The merchant must have manually
        signed the request. For more information, see Handling the
        Receipt of IPN Notifications. We recommend that you always
        verify the signature using the method in How to Verify the IPN
        Signature."""
        return self.parameters.get('signature')

    @property
    def status(self):
        """Longer description that specifies the status of the transaction.."""
        return self.parameters.get('statusCode')

    @property
    def token_id(self):
        """If notificationType is TokenCancellation, this element
        contains the ID of the cancelled token."""
        return self.parameters.get('tokenId')

    @property
    def token_type(self):
        """If notificationType is TokenCancellation, this element
        contains the type of the cancelled token."""
        return self.parameters.get('tokenType')

    @property
    def transaction_amount(self):
        """Specifies the amount payable in this transaction; for
        example, USD 10.00."""
        amount = self.parameters.get('transactionAmount')
        try:
            return decimal.Decimal(amount)
        except decimal.InvalidOperation, e:
            LOGGER.exception("Got bad transaction amount from aws: %r", amount)

    @property
    def transaction_date(self):
        """The date when this transaction occurred, specified in
        seconds since the start of the epoch."""
        timestamp = self.parameters.get('transactionDate')
        try:
            return datetime.datetime.fromtimestamp(int(timestamp))
        except ValueError, e:
            LOGGER.exception("Got bad transactionDate from aws: %r", timestamp)

    @property
    def transaction_id(self):
        """Unique ID generated by Amazon FPS for this
        transaction. This element is returned if the transaction was
        accepted by Amazon FPS."""
        return self.parameters.get('transactionId')

    @property
    def transaction_status(self):
        """An undocumented attribute that gets passed in to IPN responses.
        sigh...
        """
        status = self.parameters.get('transactionStatus')
        if status not in IPNTransactionStatusCodes:
            LOGGER.warn("Got invalid/unknown IPN Transaction Status Code: %r", status)
        return status

