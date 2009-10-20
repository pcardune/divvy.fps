README
======

The ``divvy.fps`` package provides python utilities for integrating
with Amazon.com's Flexible Payment Service.

We will go through a simple usage scenario that uses the "Basic Quick
Start" APIs.  See
http://docs.amazonwebservices.com/AmazonFPS/2008-09-17/FPSBasicGuide/
for the relevant Amazon documentation.

Configuration
-------------

Certain parameters required by ``divvy.fps`` to properly interact with
Amazon FPS can be configured globally so they do not have to be passed
in to every method call (though they can be).  Typically you will want
to start by configuring the global parameters:

  >>> from divvy.fps import conf
  >>> conf.DEFAULT_ACCESS_KEY_ID = 'this-is-a-fake-id'
  >>> conf.DEFAULT_SECRET_KEY = 'this-is-a-fake-key'

And during development, it is a good idea to set the RUN_IN_SANDBOX
option to True:

  >>> conf.RUN_IN_SANDBOX = True


Sending a Co-Branded Service Request
------------------------------------

See the relevant Amazon documentation here:
http://docs.amazonwebservices.com/AmazonFPS/2008-09-17/FPSBasicGuide/index.html?SendingaCBUIRequest.html

The first part to creating a co-branded service request involves
instantiating an authorization client, passing in your AWS access key
id and secret key.

  >>> from divvy.fps.authorization import AuthorizationClient
  >>> auth_client = AuthorizationClient()

You can then get the url for the co-branded service request page.  The
two required parameters are a return url and a transaction amount.
The method will return both the url for the co-branded service request
page and a unique caller reference for the request.

  >>> caller_ref, url = auth_client.authorize_single_use_token(
  ...     "http://www.mysite.com/thanks/for/the/order", 3.14)

If not provided as a keyword argument, the caller reference is
automatically generated using a uuid.

  >>> caller_ref
  '...'

The returned url will include all the parameters for making the
request including the signature used for validation.

  >>> url
  'https://authorize.payments-sandbox.amazon.com/cobranded-ui/actions/start?awsSignature=...%3D&callerKey=this-is-a-fake-id&callerReference=...&pipelineName=SingleUse&returnUrl=http%3A%2F%2Fwww.mysite.com%2Fthanks%2Ffor%2Fthe%2Forder&transactionAmount=3.14&version=2009-01-09'

Alternatively, you can pass in your own caller reference to use:

  >>> caller_ref, url = auth_client.authorize_single_use_token(
  ...     "http://www.mysite.com/thanks/for/the/order", 3.14,
  ...     callerReference='my-caller-reference')

  >>> caller_ref
  'my-caller-reference'

  >>> url
  'https://authorize.payments-sandbox.amazon.com/cobranded-ui/actions/start?awsSignature=DI3%2FfkEGuBzxo0gf8Sp6WQD79ks%3D&callerKey=this-is-a-fake-id&callerReference=my-caller-reference&pipelineName=SingleUse&returnUrl=http%3A%2F%2Fwww.mysite.com%2Fthanks%2Ffor%2Fthe%2Forder&transactionAmount=3.14&version=2009-01-09'


Recieving a single use token response
-------------------------------------

Once your customer has completed authorization of the payment token,
they will be redirected to the return url specified earlier.  As part
of the redirection, Amazon FPS will include information regarding the
payment token as query parameters.

``divvy.fps`` provides a wrapper object for working with the passed in
parameters.

You can instantiate a ``SingleUseTokenResponse`` object by passing in
the query parameters as a dictionary.  During construction of the
token response, the signature will be validated, and an exception
raised for an invalid signature.

    >>> sample_query_parameters = {
    ...     'status': 'SC',
    ...     'callerReference': 'some-caller-reference',
    ...     'signature': '8g9Xc+LCya3PTvDDyjJ/r3Tu2+M=',
    ...     'tokenID': 'some-token-id',
    ... }

    >>> from divvy.fps.authorization import SingleUseTokenResponse
    >>> response = SingleUseTokenResponse(sample_query_parameters)

The following attributes are then available on the response object:

    >>> response.is_success
    True

    >>> response.caller_reference
    'some-caller-reference'

    >>> response.token_id
    'some-token-id'

    >>> response.status
    'SC'

    >>> response.error_message


Making a Pay request
--------------------

Now that you have the authorization token, you want to make a pay
request.  This is done using the ApiClient.

    >>> from divvy.fps.api import ApiClient
    >>> api_client = ApiClient()

The ``pay`` method for the ApiClient has three required parameters:
the caller reference, the token id you recieved in the last step, and
the transaction amount used when creating the initial authorization
request.

    >>> response = api_client.pay('some-caller-reference',
    ...                           'some-token-id', 3.14)

What gets returned is a ``PayResponse`` object with additional
information about the payment.

    >>> response
    <PayResponse transactionId='13N8UPFET32I4I7FCF9T4ZKFETETINTK56Q' transactionStatus='Pending'>

    >>> response.transactionId
    '13N8UPFET32I4I7FCF9T4ZKFETETINTK56Q'
    >>> response.transactionStatus
    'Pending'

Recieving Instance Payment Notifications
----------------------------------------

If you are making credit card transactions, the transaction status
that comes back with a pay request will almost always be Pending.  You
won't find out about the final result of the payment until later,
using the "Instant Payment Notification" (IPN) API.

When the status of any transaction is changed by Amazon, they will
send a request to a url you specify with updated status information.
``divvy.fps`` provides a class to process this request.  We treat this
request more like an additional payment response from Amazon, so in
the python api, it is called a response.

The ``IPNResponse`` class takes a dictionary of query parameters
passed via the url that Amazon hits.

    >>> parameters = {u'status': u'SUCCESS',
    ...               u'paymentReason': u'Refund',
    ...               u'parentTransactionId': u'14GUOHEPHCAH8ZVTMEDTVUH9HLN7UISRBLK',
    ...               u'transactionDate': u'1255555956',
    ...               u'buyerEmail': u'paul@example.com',
    ...               u'transactionAmount': u'USD 9.00',
    ...               u'notificationType': u'TransactionStatus',
    ...               u'recipientEmail': u'sam@example.com',
    ...               u'callerReference': u'txnDtls906af6b8-e500-42e0-b11f-8c7f40f89c46',
    ...               u'buyerName': u'Paul',
    ...               u'signature': u'DPzwTCUGsxzmlSs00ZaWLgzgls8=',
    ...               u'recipientName': u'Sam',
    ...               u'operation': u'REFUND',
    ...               u'paymentMethod': u'CC',
    ...               u'transactionId': u'14HAFEVKQ4HT4PC9TDKND9OIB244PU3JC4I'}

    >>> from divvy.fps.api import IPNResponse
    >>> response = IPNResponse(parameters)

    >>> response.transaction_id
    u'14HAFEVKQ4HT4PC9TDKND9OIB244PU3JC4I'