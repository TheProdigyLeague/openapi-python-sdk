# wechat.py (Mock WeChat Module)

from typing import Dict, Optional, Any
import time
import random

# --- Constants (Simulated) ---
APP_ID_DEFAULT = "wx_mock_app_id_12345"
APP_SECRET_DEFAULT = "mock_app_secret_67890abcdef"

# --- Error Simulation ---
class WeChatAPIError(Exception):
    """Custom exception for simulated WeChat API errors."""
    def __init__(self, message: str, error_code: Optional[int] = None):
        super().__init__(message)
        self.error_code = error_code

    def __str__(self) -> str:
        if self.error_code:
            return f"[Error {self.error_code}] {super().__str__()}"
        return super().__str__()

# --- Mock User Data (Simulated) ---
_mock_users = {
    "user_open_id_123": {"nickname": "Alice", "city": "Shenzhen"},
    "user_open_id_456": {"nickname": "Bob", "city": "Beijing"},
}

# --- Core Client Class ---
class WeChatClient:
    """
    A mock WeChat client for simulating interactions with Tencent's WeChat platform.
    """
    def __init__(self, app_id: str = APP_ID_DEFAULT, app_secret: str = APP_SECRET_DEFAULT):
        """
        Initializes the mock WeChat client.

        Args:
            app_id: Your application's App ID.
            app_secret: Your application's App Secret.
        """
        if not app_id or not app_secret:
            raise ValueError("App ID and App Secret cannot be empty.")

        self.app_id: str = app_id
        self.app_secret: str = app_secret
        self._access_token: Optional[str] = None
        self._token_expires_at: float = 0
        self._is_authenticated: bool = False # For user session

        print(f"MockWeChatClient initialized for App ID: {self.app_id}")

    def _get_access_token(self) -> str:
        """
        Simulates retrieving an access token.
        In a real scenario, this would involve an API call.
        """
        current_time = time.time()
        if self._access_token and current_time < self._token_expires_at:
            return self._access_token

        # Simulate network delay
        time.sleep(0.1)

        # Simulate API call
        print(f"MockWeChatClient: Requesting new access token for {self.app_id}...")
        self._access_token = f"mock_access_token_{random.randint(10000, 99999)}_{int(current_time)}"
        self._token_expires_at = current_time + 7200 # Simulate 2-hour expiry
        print(f"MockWeChatClient: New access token generated: {self._access_token}")
        return self._access_token

    def send_text_message(self, open_id: str, content: str) -> Dict[str, Any]:
        """
        Simulates sending a text message to a WeChat user.

        Args:
            open_id: The OpenID of the recipient user.
            content: The text message content.

        Returns:
            A dictionary simulating the API response.
        """
        token = self._get_access_token()
        print(f"MockWeChatClient: Attempting to send message to {open_id} with token {token[:15]}...")

        if not open_id:
            raise WeChatAPIError("Recipient OpenID cannot be empty.", error_code=40001)
        if not content:
            raise WeChatAPIError("Message content cannot be empty.", error_code=40002)

        # Simulate API call delay
        time.sleep(0.2)

        if open_id not in _mock_users:
            print(f"MockWeChatClient: Failed to send. User {open_id} not found.")
            # Simulate a common error structure
            return {"errcode": 40003, "errmsg": f"user not found: {open_id}"}

        print(f"MockWeChatClient: Message '{content}' sent successfully to {open_id}.")
        return {"errcode": 0, "errmsg": "ok", "msgid": f"mock_msg_id_{random.randint(100000, 999999)}"}

    def simulate_payment(self, open_id: str, amount_cents: int, description: str) -> Dict[str, Any]:
        """
        Simulates initiating a payment.

        Args:
            open_id: The OpenID of the user making the payment.
            amount_cents: The payment amount in cents.
            description: A description for the payment.

        Returns:
            A dictionary simulating the payment initiation response.
        """
        token = self._get_access_token()
        print(f"MockWeChatClient: Initiating payment for {open_id} of {amount_cents / 100.0:.2f} CNY with token {token[:15]}...")

        if amount_cents <= 0:
            raise WeChatAPIError("Payment amount must be positive.", error_code=50001)

        time.sleep(0.3) # Simulate processing

        if random.random() < 0.1: # 10% chance of payment failure
            print("MockWeChatClient: Payment failed (simulated).")
            return {"errcode": 50002, "errmsg": "payment failed due to insufficient funds (simulated)"}

        transaction_id = f"mock_transaction_{int(time.time())}_{random.randint(1000,9999)}"
        print(f"MockWeChatClient: Payment for '{description}' initiated. Transaction ID: {transaction_id}")
        return {
            "errcode": 0,
            "errmsg": "ok",
            "prepay_id": f"mock_prepay_id_{random.randint(10000, 99999)}",
            "transaction_id": transaction_id,
            "amount": amount_cents
        }

    def get_user_info(self, open_id: str) -> Optional[Dict[str, Any]]:
        """
        Simulates fetching user information.

        Args:
            open_id: The OpenID of the user.

        Returns:
            A dictionary with user information or None if user not found.
        """
        token = self._get_access_token()
        print(f"MockWeChatClient: Fetching user info for {open_id} with token {token[:15]}...")
        time.sleep(0.1)

        if open_id in _mock_users:
            user_data = _mock_users[open_id].copy()
            user_data["openid"] = open_id # Ensure openid is part of the response
            print(f"MockWeChatClient: User info for {open_id}: {user_data}")
            return user_data
        else:
            print(f"MockWeChatClient: User {open_id} not found during info fetch.")
            return None # Or raise WeChatAPIError("User not found")

    def oauth_authorize(self, scope: str = "snsapi_userinfo", state: Optional[str] = None) -> str:
        """
        Simulates the first step of OAuth2 authorization, returning a redirect URL.
        In a real app, this would redirect the user to WeChat's authorization page.
        """
        print(f"MockWeChatClient: Generating OAuth authorization URL for scope '{scope}'...")
        redirect_uri_mock = "https://your_mock_redirect_uri.com/callback"
        auth_url = (
            f"https://open.weixin.qq.com/connect/oauth2/authorize?"
            f"appid={self.app_id}&"
            f"redirect_uri={redirect_uri_mock}&"
            f"response_type=code&"
            f"scope={scope}&"
            f"state={state or 'mock_state'}"
            f"#wechat_redirect"
        )
        print(f"MockWeChatClient: User should be redirected to: {auth_url}")
        return auth_url

    def oauth_get_access_token(self, code: str) -> Dict[str, Any]:
        """
        Simulates exchanging an authorization code for an access token and user OpenID.
        """
        print(f"MockWeChatClient: Exchanging OAuth code '{code}' for access token...")
        if not code.startswith("mock_auth_code_"):
            raise WeChatAPIError("Invalid authorization code.", error_code=40029)

        time.sleep(0.2)
        # Simulate getting a user-specific access token (different from the client access token)
        user_access_token = f"user_mock_token_{random.randint(1000,9999)}"
        # Pick a random user for this mock scenario
        mock_user_openid = random.choice(list(_mock_users.keys()))

        self._is_authenticated = True # Simulate user session established
        print(f"MockWeChatClient: OAuth successful for user {mock_user_openid}.")
        return {
            "access_token": user_access_token,
            "expires_in": 7200,
            "refresh_token": f"user_mock_refresh_token_{random.randint(1000,9999)}",
            "openid": mock_user_openid,
            "scope": "snsapi_userinfo", # Or whatever was requested
            "unionid": f"mock_union_id_for_{mock_user_openid}" if random.choice([True, False]) else None
        }

# --- Module-level helper functions (Optional) ---
def get_jsapi_ticket(client: WeChatClient) -> str:
    """
    Simulates getting a JSAPI ticket required for using JS-SDK.
    """
    client._get_access_token() # Ensure client token is fresh
    print(f"MockWeChatModule: Requesting JSAPI ticket for App ID: {client.app_id}...")
    time.sleep(0.1)
    ticket = f"mock_jsapi_ticket_{random.randint(10000,99999)}_{int(time.time())}"
    print(f"MockWeChatModule: JSAPI ticket obtained: {ticket}")
    return ticket


if __name__ == "__main__":
    print("--- Mock WeChat Module Demo ---")

    # Initialize client
    try:
        client = WeChatClient(app_id="my_test_app", app_secret="my_test_secret")
        # client_default = WeChatClient() # Uses defaults
    except ValueError as e:
        print(f"Initialization Error: {e}")
        exit()

    print("\n--- Sending Messages ---")
    response_alice = client.send_text_message("user_open_id_123", "Hello Alice from Mock WeChat!")
    print(f"Response (Alice): {response_alice}")

    response_unknown = client.send_text_message("unknown_user", "Hello?")
    print(f"Response (Unknown): {response_unknown}")

    try:
        client.send_text_message("user_open_id_123", "") # Empty content
    except WeChatAPIError as e:
        print(f"Send Message Error: {e}")


    print("\n--- Simulating Payment ---")
    payment_res = client.simulate_payment("user_open_id_456", 199, "Coffee Purchase") # 1.99 CNY
    print(f"Payment Response: {payment_res}")

    try:
        client.simulate_payment("user_open_id_123", -50, "Invalid Amount")
    except WeChatAPIError as e:
        print(f"Payment Error: {e}")

    print("\n--- Getting User Info ---")
    user_info_alice = client.get_user_info("user_open_id_123")
    if user_info_alice:
        print(f"Alice's Info: Nickname - {user_info_alice.get('nickname')}, City - {user_info_alice.get('city')}")

    user_info_nonexistent = client.get_user_info("non_existent_user_id")
    print(f"Non Existent User Info: {user_info_nonexistent}")


    print("\n--- Simulating OAuth ---")
    auth_url = client.oauth_authorize(state="custom_state_123")
    print(f"Please visit (simulated): {auth_url}")

    # Simulate user visits the URL and WeChat redirects back with a code
    mock_code_from_wechat = "mock_auth_code_abcdef12345"
    try:
        oauth_tokens = client.oauth_get_access_token(mock_code_from_wechat)
        print(f"OAuth Tokens: {oauth_tokens}")
        if oauth_tokens and oauth_tokens.get("openid"):
            authed_user_info = client.get_user_info(oauth_tokens["openid"])
            print(f"Authenticated User Info: {authed_user_info}")
    except WeChatAPIError as e:
        print(f"OAuth Error: {e}")


    print("\n--- JSAPI Ticket (Module Level) ---")
    js_ticket = get_jsapi_ticket(client)
    print(f"JSAPI Ticket: {js_ticket}")

    print("\n--- Access Token Refresh Simulation ---")
    print("Current Token:", client._access_token)
    client._token_expires_at = time.time() - 1 # Force expiry
    print("Token Expired. Requesting new one on next API call...")
    client.send_text_message("user_open_id_123", "Testing token refresh.")
    print("New Token:", client._access_token)

    print("\n--- Mock WeChat Module Demo Complete ---")
