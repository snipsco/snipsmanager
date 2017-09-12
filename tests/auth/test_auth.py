from unittest import TestCase
from snipsskills.utils.assistant_downloader import AuthDownloader, AuthExceptionInvalidCredentials, AuthExceptionInvalidAssistantId

class AuthTest(TestCase):
    def setUp(self):
        pass

class AuthTest(TestCase):
    def test_input_wrong_email(self):
        with self.assertRaises(AuthExceptionInvalidCredentials):
            AuthDownloader("anthony", "password123", "proj_xxxxxxxxx")

        with self.assertRaises(AuthExceptionInvalidCredentials):
            AuthDownloader("anthony.test", "password123", "proj_xxxxxxxxx")

        with self.assertRaises(AuthExceptionInvalidCredentials):
            AuthDownloader("anthony.test@test", "password123", "proj_xxxxxxxxx")

        with self.assertRaises(AuthExceptionInvalidCredentials):
            AuthDownloader("anthony.test@provider.", "password123", "proj_xxxxxxxxx")

    def test_input_password(self):
        with self.assertRaises(AuthExceptionInvalidCredentials):
            AuthDownloader("anthony.test@provider.com", "", "proj_xxxxxxxxx")

    def test_input_assistantId(self):
        with self.assertRaises(AuthExceptionInvalidAssistantId):
            AuthDownloader("user.test@provider.com","password123", "proj_")

