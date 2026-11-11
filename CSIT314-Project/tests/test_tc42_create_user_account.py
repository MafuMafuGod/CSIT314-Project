"""TC42 — Create a User Account."""
from tests.user_admin_tc_helpers import BaseUserAdminTest
from entity import UserAccount


class TC42CreateUserAccount(BaseUserAdminTest):
    def test_TC42_01_create_form_is_available_to_admin(self):
        response, html = self.getText("/admin/users/create")
        self.assertEqual(response.status_code, 200)
        self.assertIn("Create user", html)
        self.assertIn('name="name"', html)
        self.assertIn('name="u"', html)

    def test_TC42_02_valid_details_create_account_with_selected_profile(self):
        _, html = self.postText("/admin/users/create", data={
            "name": "Mei Tan", "u": "mei.tan@example.com", "p": "StrongPass123!",
            "profile": "designer", "permissions": ["Manage own IDPs"],
        })
        account = UserAccount.selectUserAccount("mei.tan@example.com")
        self.assertIn("created successfully", html)
        self.assertEqual(account["name"], "Mei Tan")
        self.assertEqual(account["profile"], "designer")
        self.assertEqual(account["permissions"], ["Manage own IDPs"])
        self.assertEqual(account["status"], "active")

    def test_TC42_03_missing_or_invalid_details_show_validation_without_creating(self):
        before = len(UserAccount.getAllAccounts())
        _, html = self.postText("/admin/users/create", data={
            "name": "", "u": "not-an-email", "p": "StrongPass123!", "profile": "designer",
        })
        self.assertIn("Please enter the user&#39;s name.", html)
        self.assertIn("Please enter a valid email address.", html)
        self.assertEqual(len(UserAccount.getAllAccounts()), before)

    def test_TC42_04_duplicate_email_is_rejected(self):
        before = len(UserAccount.getAllAccounts())
        _, html = self.postText("/admin/users/create", data={
            "name": "Duplicate", "u": "designer@4reno.com", "p": "SomePass123!",
            "profile": "designer", "permissions": ["Manage own IDPs"],
        })
        self.assertIn("already exists", html)
        self.assertEqual(len(UserAccount.getAllAccounts()), before)


if __name__ == "__main__":
    import unittest
    unittest.main()
