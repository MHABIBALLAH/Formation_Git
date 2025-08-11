import unittest
import json
import os

from src.api.app import create_app
from src.api.extensions import db, bcrypt
from src.core.auth.models import User

class AuthTestCase(unittest.TestCase):

    def setUp(self):
        """Set up a test client and a new database for each test."""
        self.app = create_app('src.config.TestingConfig')
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        """Clean up the database after each test."""
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def _register_user(self, username="testuser", password="password"):
        """Helper function to register a user."""
        return self.client.post(
            '/api/auth/register',
            data=json.dumps(dict(username=username, password=password)),
            content_type='application/json'
        )

    def _login_user(self, username="testuser", password="password"):
        """Helper function to log in a user."""
        return self.client.post(
            '/api/auth/login',
            data=json.dumps(dict(username=username, password=password)),
            content_type='application/json'
        )

    def test_registration_success(self):
        """Test user registration successfully creates a new user."""
        res = self._register_user()
        self.assertEqual(res.status_code, 201)
        user = User.query.filter_by(username="testuser").first()
        self.assertIsNotNone(user)
        self.assertTrue(bcrypt.check_password_hash(user.password_hash, "password"))

    def test_registration_duplicate_username(self):
        """Test registration fails with a duplicate username."""
        self._register_user()
        res = self._register_user()
        self.assertEqual(res.status_code, 409)

    def test_login_success(self):
        """Test user can log in with correct credentials."""
        self._register_user()
        res = self._login_user()
        self.assertEqual(res.status_code, 200)

    def test_login_invalid_password(self):
        """Test login fails with an incorrect password."""
        self._register_user()
        res = self._login_user(password="wrongpassword")
        self.assertEqual(res.status_code, 401)

    def test_login_nonexistent_user(self):
        """Test login fails for a user that does not exist."""
        res = self._login_user(username="nouser")
        self.assertEqual(res.status_code, 401)

    def test_access_protected_route_without_login(self):
        """Test that a protected route returns 401 Unauthorized without login."""
        res = self.client.get('/api/summary')
        self.assertEqual(res.status_code, 401)
        data = json.loads(res.data)
        self.assertEqual(data['error'], 'Authentication required')

    def test_access_protected_route_with_login(self):
        """Test that a protected route can be accessed after logging in."""
        self._register_user()
        self._login_user()
        res = self.client.get('/api/summary')
        self.assertEqual(res.status_code, 200)
        self.assertIn(b'total_revenue', res.data)

    def test_logout(self):
        """Test that a user can log out and lose access to protected routes."""
        self._register_user()
        self._login_user()
        res_logout = self.client.post('/api/auth/logout')
        self.assertEqual(res_logout.status_code, 200)
        res_after_logout = self.client.get('/api/auth/profile')
        self.assertEqual(res_after_logout.status_code, 401)
        data = json.loads(res_after_logout.data)
        self.assertEqual(data['error'], 'Authentication required')

    def test_change_password(self):
        """Test changing a user's password."""
        self._register_user()
        self._login_user()

        # Case 1: Wrong old password
        res_wrong = self.client.post(
            '/api/auth/change-password',
            data=json.dumps(dict(old_password="wrong", new_password="newpassword")),
            content_type='application/json'
        )
        self.assertEqual(res_wrong.status_code, 403)
        self.assertIn(b'Invalid old password', res_wrong.data)

        # Case 2: Successful password change
        res_success = self.client.post(
            '/api/auth/change-password',
            data=json.dumps(dict(old_password="password", new_password="newpassword")),
            content_type='application/json'
        )
        self.assertEqual(res_success.status_code, 200)
        self.assertIn(b'Password updated successfully', res_success.data)

        # Verify the new password works for login
        self.client.post('/api/auth/logout') # Logout first
        res_login_new = self._login_user(password="newpassword")
        self.assertEqual(res_login_new.status_code, 200)

if __name__ == '__main__':
    unittest.main()
