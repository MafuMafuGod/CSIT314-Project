"""TC49 — Update a User Profile."""
from unittest.mock import patch

from tests.user_admin_tc_helpers import BaseUserAdminTest
from entity import UserProfile


class TC49UpdateUserProfile(BaseUserAdminTest):
    def test_TC49_01_edit_form_shows_current_profile(self):
        response, html = self.getText("/admin/profiles/edit/Customer")
        self.assertEqual(response.status_code, 200)
        self.assertIn('value="Customer"', html)
        self.assertIn("Homeowners looking for an interior designer", html)

    def test_TC49_02_valid_changes_are_saved_and_confirmed(self):
        _, html = self.postText("/admin/profiles/edit/Customer", data={
            "name": "Homeowner", "description": "Updated role", "permissions": ["Search IDPs"],
        })
        profile = UserProfile.selectProfile("Homeowner")
        self.assertIn("Customer → Homeowner", html)
        self.assertEqual(profile["description"], "Updated role")
        self.assertEqual(profile["permissions"], ["Search IDPs"])

    def test_TC49_03_save_failure_does_not_report_success_or_change_profile(self):
        with patch("boundary.update_user_profile_page.UpdateUserProfileController.updateUserProfile",
                   return_value=False):
            _, html = self.postText("/admin/profiles/edit/Customer", data={
                "name": "Customer Updated", "description": "Should not save",
                "permissions": ["Search IDPs"],
            })
        self.assertIn("The profile could not be saved. Please try again.", html)
        self.assertNotIn("<h2>What changed</h2>", html)
        profile = UserProfile.selectProfile("Customer")
        self.assertEqual(profile["description"], "Homeowners looking for an interior designer")
        self.assertEqual(profile["permissions"], ["Search IDPs", "View IDP details", "Manage shortlist"])


if __name__ == "__main__":
    import unittest
    unittest.main()
