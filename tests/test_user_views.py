"""
Base Test case with setup and methods that other
test classes inherit
"""
import unittest
import json
import datetime

from app import create_app

class AuthTestCase(unittest.TestCase):
    """Base Test Case"""
    def setUp(self):
        """Set up test variables"""
        self.app = create_app(config_name="testing")
        self.client = self.app.test_client()
        self.user_data = {
            "email":"muthama@gmail.com",
            "username":"admini",
            "password":"jusTifiable1@"
        }
        self.login_data = {
            "email":"muthamas@gmail.com",
            "username":"adminini",
            "password":"jusTifiablyte1@"
        }
        self.header = {'Content-Type': 'application/json'}

    def test_registration(self):
        """Test user registration works correcty."""
        res = self.client.post('/auth/register', headers=self.header, data=json.dumps(self.user_data))
        result = json.loads(res.data.decode())
        self.assertEqual(result['message'], "Account created successfully")
        self.assertEqual(res.status_code, 201)

    def test_login(self):
        """Test user registration works correcty."""
        self.client.post('/auth/register', headers=self.header, data=json.dumps(self.login_data))
        res = self.client.post('/auth/login', headers=self.header, data=json.dumps(self.login_data))
        result = json.loads(res.data.decode())
        self.assertEqual(result['message'], "Login successfull")
        self.assertEqual(res.status_code, 200)

if __name__ == "__main__":
    unittest.main()