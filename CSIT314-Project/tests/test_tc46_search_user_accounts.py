"""TC46 — Search User Accounts."""
from tests.user_admin_tc_helpers import BaseUserAdminTest
from entity import UserAccount


class TC46SearchUserAccounts(BaseUserAdminTest):
    def test_TC46_01_search_by_name_or_email(self):
        _, html = self.getText("/admin/users?q=daniel")
        self.assertIn("Daniel Lim", html)
        self.assertNotIn("Hannah Tan", html)

        _, html = self.getText("/admin/users?q=designer%40")
        self.assertIn("designer@4reno.com", html)
        self.assertNotIn("customer@4reno.com", html)

    def test_TC46_02_search_by_profile_and_status(self):
        UserAccount.suspendAccount("customer@4reno.com", "test filter")
        _, html = self.getText("/admin/users?profile=designer&status=active")
        self.assertIn("designer@4reno.com", html)
        self.assertNotIn("customer@4reno.com", html)
        self.assertNotIn("admin@4reno.com", html)

    def test_TC46_03_no_match_shows_empty_state(self):
        _, html = self.getText("/admin/users?q=no-such-user-987")
        self.assertIn("No user accounts found", html)
        self.assertNotIn("designer@4reno.com", html)


if __name__ == "__main__":
    import unittest
    unittest.main()
