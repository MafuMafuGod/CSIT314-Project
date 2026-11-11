"""TC47 — Create a User Profile."""
from tests.user_admin_tc_helpers import BaseUserAdminTest
from entity import UserProfile


class TC47CreateUserProfile(BaseUserAdminTest):
    def test_TC47_01_create_profile_form_is_available(self):
        response, html = self.getText("/admin/profiles/create")
        self.assertEqual(response.status_code, 200)
        self.assertIn("Create profile", html)
        self.assertIn('name="name"', html)

    def test_TC47_02_valid_profile_and_permissions_are_saved(self):
        _, html = self.postText("/admin/profiles/create", data={
            "name": "Senior Admin", "description": "Audit access",
            "permissions": ["View audit log"],
        })
        profile = UserProfile.selectProfile("Senior Admin")
        self.assertIn("Profile summary", html)
        self.assertEqual(profile["description"], "Audit access")
        self.assertEqual(profile["permissions"], ["View audit log"])

    def test_TC47_03_missing_details_or_unknown_permission_are_rejected(self):
        before = len(UserProfile.getAllProfiles())
        _, html = self.postText("/admin/profiles/create", data={"name": "", "permissions": []})
        self.assertIn("Please enter a profile name.", html)
        self.assertIn("Please select at least one permission.", html)
        self.assertEqual(len(UserProfile.getAllProfiles()), before)

        _, html = self.postText("/admin/profiles/create", data={
            "name": "Invalid Role", "permissions": ["Unknown permission"],
        })
        self.assertIn("Please choose permissions from the list.", html)
        self.assertEqual(UserProfile.selectProfile("Invalid Role"), {})


if __name__ == "__main__":
    import unittest
    unittest.main()
