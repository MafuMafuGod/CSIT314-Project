"""TC48 — View a User Profile."""
from tests.user_admin_tc_helpers import BaseUserAdminTest
from entity import UserProfile


class TC48ViewUserProfile(BaseUserAdminTest):
    def test_TC48_01_profile_list_is_displayed(self):
        response, html = self.getText("/admin/profiles")
        self.assertEqual(response.status_code, 200)
        self.assertIn("Interior Designer", html)
        self.assertIn("User Admin", html)

    def test_TC48_02_selected_profile_shows_description_permissions_and_users(self):
        _, html = self.getText("/admin/profiles/view/Interior%20Designer")
        self.assertIn("Designers who publish IDPs", html)
        self.assertIn("Manage own IDPs", html)
        self.assertIn("designer@4reno.com", html)

    def test_TC48_03_empty_profile_list_has_clear_message(self):
        UserProfile._profiles = []
        _, html = self.getText("/admin/profiles")
        self.assertIn("No user profiles available", html)


if __name__ == "__main__":
    import unittest
    unittest.main()
