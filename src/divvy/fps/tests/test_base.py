import unittest
import random

from divvy.fps import base
from divvy.fps import util

class AuthorizationClientTestCase(unittest.TestCase):

    def setUp(self):
        base.RANDOM = random.Random(1)

    def test_validate_signature(self):
        client = base.AmazonFPSClient(
            access_key_id="1DSE1XP1AXT7YPP0P702",
            secret_key="G8FWjm4ZfxEMGdn+BupwnQQ+W78BJE1dWptxkZeE")

        sig = util.get_signature(client.secret_key, {"foo":"bar"})

        self.assertTrue(client.validate_signature({"foo":"bar","signature":sig}))
        self.assertFalse(client.validate_signature({"foo":"baz","signature":sig}))

        self.assertTrue(client.validate_signature({"foo":"bar"}, signature=sig))
        self.assertFalse(client.validate_signature({"foo":"baz"}, signature=sig))
