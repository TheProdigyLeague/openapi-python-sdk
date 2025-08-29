# 10c3n7/unittest.py
import unittest
import time
from unittest.mock import patch # For mocking time.sleep or random if needed

# Adjust the import based on how you run your tests and your PYTHONPATH
# If running tests from the directory *above* 10c3n7:
from . import wechat  # Relative import within the package
# Or, if 10c3n7 is directly in PYTHONPATH:
# import 10c3n7.wechat as wechat

class TestWeChatClient(unittest.TestCase):

    def setUp(self):
        """Set up for each test method."""
        # Using specific IDs for predictable testing
        self.test_app_id = "test_app_123"
        self.test_app_secret = "test_secret_xyz"
        self.client = wechat.WeChatClient(app_id=self.test_app_id, app_secret=self.test_app_secret)
        # Reset any shared mock data if necessary (though _mock_users is module-level)
        # For simplicity, we'll rely on the initial state of _mock_users
        self.known_user_id = "user_open_id_123" # From wechat.py's _mock_users
        self.unknown_user_id = "non_existent_user_999"

    def test_client_initialization(self):
        self.assertEqual(self.client.app_id, self.test_app_id)
        self.assertEqual(self.client.app_secret, self.test_app_secret)
        self.assertIsNone(self.client._access_token) # Initially no token

    def test_client_initialization_with_defaults(self):
        default_client = wechat.WeChatClient()
        self.assertEqual(default_client.app_id, wechat.APP_ID_DEFAULT)
        self.assertEqual(default_client.app_secret, wechat.APP_SECRET_DEFAULT)

    def test_client_initialization_empty_credentials(self):
        with self.assertRaisesRegex(ValueError, "App ID and App Secret cannot be empty"):
            wechat.WeChatClient(app_id="", app_secret="some_secret")
        with self.assertRaisesRegex(ValueError, "App ID and App Secret cannot be empty"):
            wechat.WeChatClient(app_id="some_id", app_secret="")

    def test_get_access_token_retrieval_and_caching(self):
        # First call should generate a token
        token1 = self.client._get_access_token() # Accessing protected for testing is common
        self.assertIsNotNone(token1)
        self.assertTrue(token1.startswith("mock_access_token_"))
        self.assertGreater(self.client._token_expires_at, time.time())

        # Second call immediately after should return the cached token
        token2 = self.client._get_access_token()
        self.assertEqual(token1, token2)

        # Force expiry and check if a new token is generated
        self.client._token_expires_at = time.time() - 100 # Expire the token
        token3 = self.client._get_access_token()
        self.assertIsNotNone(token3)
        self.assertNotEqual(token1, token3)

    def test_send_text_message_success(self):
        response = self.client.send_text_message(self.known_user_id, "Test message")
        self.assertEqual(response["errcode"], 0)
        self.assertEqual(response["errmsg"], "ok")
        self.assertTrue("msgid" in response)

    def test_send_text_message_user_not_found(self):
        response = self.client.send_text_message(self.unknown_user_id, "Test message")
        self.assertEqual(response["errcode"], 40003)
        self.assertIn("user not found", response["errmsg"])

    def test_send_text_message_empty_content(self):
        with self.assertRaisesRegex(wechat.WeChatAPIError, "Message content cannot be empty"):
            self.client.send_text_message(self.known_user_id, "")

    def test_send_text_message_empty_openid(self):
        with self.assertRaisesRegex(wechat.WeChatAPIError, "Recipient OpenID cannot be empty"):
            self.client.send_text_message("", "Some message")

    def test_simulate_payment_success(self):
        response = self.client.simulate_payment(self.known_user_id, 100, "Test Payment") # 1.00 CNY
        self.assertEqual(response["errcode"], 0)
        self.assertEqual(response["errmsg"], "ok")
        self.assertTrue("prepay_id" in response)
        self.assertTrue("transaction_id" in response)
        self.assertEqual(response["amount"], 100)

    def test_simulate_payment_zero_amount(self):
        with self.assertRaisesRegex(wechat.WeChatAPIError, "Payment amount must be positive"):
            self.client.simulate_payment(self.known_user_id, 0, "Zero Payment")

    def test_simulate_payment_negative_amount(self):
        with self.assertRaisesRegex(wechat.WeChatAPIError, "Payment amount must be positive"):
            self.client.simulate_payment(self.known_user_id, -50, "Negative Payment")

    @patch('random.random', return_value=0.05) # Ensure payment fails (if < 0.1)
    def test_simulate_payment_simulated_failure(self, mock_random):
        response = self.client.simulate_payment(self.known_user_id, 200, "Payment Expected to Fail")
        self.assertEqual(response["errcode"], 50002)
        self.assertIn("payment failed", response["errmsg"])

    def test_get_user_info_success(self):
        user_info = self.client.get_user_info(self.known_user_id)
        self.assertIsNotNone(user_info)
        self.assertEqual(user_info["openid"], self.known_user_id)
        self.assertEqual(user_info["nickname"], wechat._mock_users[self.known_user_id]["nickname"])

    def test_get_user_info_not_found(self):
        user_info = self.client.get_user_info(self.unknown_user_id)
        self.assertIsNone(user_info)

    def test_oauth_authorize(self):
        auth_url = self.client.oauth_authorize(scope="snsapi_base", state="my_state_123")
        self.assertIn(f"appid={self.test_app_id}", auth_url)
        self.assertIn("scope=snsapi_base", auth_url)
        self.assertIn("state=my_state_123", auth_url)
        self.assertTrue(auth_url.startswith("https://open.weixin.qq.com/connect/oauth2/authorize"))

    def test_oauth_get_access_token_success(self):
        mock_code = "mock_auth_code_test123"
        response = self.client.oauth_get_access_token(mock_code)
        self.assertIn("access_token", response)
        self.assertIn("openid", response)
        self.assertTrue(response["openid"] in wechat._mock_users) # Check if a valid mock user was chosen
        self.assertTrue(self.client._is_authenticated)

    def test_oauth_get_access_token_invalid_code(self):
        with self.assertRaisesRegex(wechat.WeChatAPIError, "Invalid authorization code"):
            self.client.oauth_get_access_token("invalid_code_format")

    def test_get_jsapi_ticket(self):
        # This function is module-level, so it needs the client instance
        ticket = wechat.get_jsapi_ticket(self.client)
        self.assertIsNotNone(ticket)
        self.assertTrue(ticket.startswith("mock_jsapi_ticket_"))
        self.assertIsNotNone(self.client._access_token, "Client access token should be fetched by get_jsapi_ticket")

if __name__ == '__main__':
    unittest.main()
