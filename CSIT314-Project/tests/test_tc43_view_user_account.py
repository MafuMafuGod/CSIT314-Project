"""TC43 — View a User Account."""
from tests.user_admin_tc_helpers import BaseUserAdminTest


class TC43ViewUserAccount(BaseUserAdminTest):
    def test_TC43_01_user_account_list_is_displayed(self):
        _, html = self.getText("/admin/users")
        self.assertIn("User Management", html)
        self.assertIn("customer@4reno.com", html)
        self.assertIn("designer@4reno.com", html)

    def test_TC43_02_selected_account_details_are_displayed_without_password(self):
        _, html = self.getText("/admin/users/view/designer@4reno.com")
        self.assertIn("Daniel Lim", html)
        self.assertIn("designer@4reno.com", html)
        self.assertIn("Interior Designer", html)
        self.assertIn("Active", html)
        self.assertNotIn("design123", html)

    def test_TC43_03_non_admin_cannot_view_account_details(self):
        customer = self.loginAs("customer@4reno.com", "password123")
        response, _ = self.getText("/admin/users/view/designer@4reno.com", browser=customer,
                                   follow_redirects=False)
        self.assertEqual(response.status_code, 302)
        self.assertNotIn("/admin/users/view/", response.headers.get("Location", ""))


if __name__ == "__main__":
    import unittest
    unittest.main()
