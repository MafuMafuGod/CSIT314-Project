"""TC44 — Update a User Account."""
from tests.user_admin_tc_helpers import BaseUserAdminTest
from entity import UserAccount


class TC44UpdateUserAccount(BaseUserAdminTest):
    def test_TC44_01_edit_form_shows_current_details(self):
        response, html = self.getText("/admin/users/edit/customer@4reno.com")
        self.assertEqual(response.status_code, 200)
        self.assertIn('value="Hannah Tan"', html)
        self.assertIn('value="customer@4reno.com"', html)

    def test_TC44_02_valid_changes_are_saved_and_confirmed(self):
        _, html = self.postText("/admin/users/edit/customer@4reno.com", data={
            "name": "Hannah T", "u": "hannah.t@example.com", "profile": "customer",
            "permissions": ["Search IDPs", "View IDP details"],
        })
        account = UserAccount.selectUserAccount("hannah.t@example.com")
        self.assertIn("What changed", html)
        self.assertIn("Hannah Tan", html)
        self.assertEqual(account["name"], "Hannah T")
        self.assertEqual(account["permissions"], ["Search IDPs", "View IDP details"])

    def test_TC44_03_invalid_details_are_not_saved(self):
        _, html = self.postText("/admin/users/edit/customer@4reno.com", data={
            "name": "", "u": "invalid-email", "profile": "customer",
            "permissions": ["Search IDPs"],
        })
        self.assertIn("Please enter the user&#39;s name.", html)
        self.assertIn("Please enter a valid email address.", html)
        account = UserAccount.selectUserAccount("customer@4reno.com")
        self.assertEqual(account["name"], "Hannah Tan")
        self.assertEqual(account["u"], "customer@4reno.com")


if __name__ == "__main__":
    import unittest
    unittest.main()
