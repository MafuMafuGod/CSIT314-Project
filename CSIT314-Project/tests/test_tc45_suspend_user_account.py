"""TC45 — Suspend a User Account."""
from tests.user_admin_tc_helpers import BaseUserAdminTest
from entity import UserAccount


class TC45SuspendUserAccount(BaseUserAdminTest):
    def test_TC45_01_and_02_confirm_suspension_and_block_existing_session(self):
        customer = self.loginAs("customer@4reno.com", "password123")
        _, html = self.postText("/admin/users/suspend/customer@4reno.com",
                                data={"reason": "Account review"})
        account = UserAccount.selectUserAccount("customer@4reno.com")
        self.assertIn("has been suspended", html)
        self.assertEqual(account["status"], "suspended")
        self.assertEqual(account["suspendReason"], "Account review")

        _, blocked_html = self.getText("/", browser=customer)
        self.assertIn("Your account has been suspended", blocked_html)

    def test_TC45_03_non_admin_cannot_suspend_an_account(self):
        customer = self.loginAs("customer@4reno.com", "password123")
        response, _ = self.postText("/admin/users/suspend/designer@4reno.com",
                                    data={"reason": "Unauthorized"}, browser=customer,
                                    follow_redirects=False)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(UserAccount.selectUserAccount("designer@4reno.com")["status"], "active")


if __name__ == "__main__":
    import unittest
    unittest.main()
