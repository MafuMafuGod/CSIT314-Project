"""TC50 — Suspend a User Profile."""
from tests.user_admin_tc_helpers import BaseUserAdminTest
from entity import UserProfile


class TC50SuspendUserProfile(BaseUserAdminTest):
    def test_TC50_01_and_02_confirm_suspension_and_block_profile_users(self):
        customer = self.loginAs("customer@4reno.com", "password123")
        _, html = self.postText("/admin/profiles/suspend/Customer", data={"reason": "Role review"})
        profile = UserProfile.selectProfile("Customer")
        self.assertIn("has been suspended", html)
        self.assertEqual(profile["status"], "suspended")
        self.assertEqual(profile["suspendReason"], "Role review")

        _, blocked_html = self.getText("/", browser=customer)
        self.assertIn("Your account has been suspended", blocked_html)

    def test_TC50_03_non_admin_cannot_suspend_a_profile(self):
        customer = self.loginAs("customer@4reno.com", "password123")
        response, _ = self.postText("/admin/profiles/suspend/Interior%20Designer",
                                    data={"reason": "Unauthorized"}, browser=customer,
                                    follow_redirects=False)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(UserProfile.selectProfile("Interior Designer")["status"], "active")


if __name__ == "__main__":
    import unittest
    unittest.main()
