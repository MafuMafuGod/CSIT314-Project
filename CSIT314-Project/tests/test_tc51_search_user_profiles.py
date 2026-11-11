"""TC51 — Search User Profiles."""
from tests.user_admin_tc_helpers import BaseUserAdminTest
from entity import UserProfile


class TC51SearchUserProfiles(BaseUserAdminTest):
    def test_TC51_01_search_by_profile_name(self):
        _, html = self.getText("/admin/profiles?q=interior")
        self.assertIn("Interior Designer", html)
        self.assertNotIn("Platform Management</a>", html)

    def test_TC51_02_search_by_status_and_name_together(self):
        UserProfile.suspendProfile("Customer", "test filter")
        _, html = self.getText("/admin/profiles?q=customer&status=active")
        self.assertIn("No user profiles found", html)
        _, html = self.getText("/admin/profiles?status=active")
        self.assertIn("Interior Designer", html)
        self.assertNotIn("Customer</a>", html)

    def test_TC51_03_no_match_shows_empty_state(self):
        _, html = self.getText("/admin/profiles?q=no-such-profile-987")
        self.assertIn("No user profiles found", html)
        self.assertNotIn("Interior Designer</a>", html)


if __name__ == "__main__":
    import unittest
    unittest.main()
