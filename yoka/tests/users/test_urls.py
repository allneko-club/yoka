from django.test import TestCase
from django.urls import reverse


class TestUsersURLs(TestCase):
    """urls.pyのテスト"""

    def test_login_url(self):
        self.assertURLEqual(reverse("users:login"), "/login/")

    def test_logout_url(self):
        self.assertURLEqual(reverse("users:logout"), "/logout/")

    def test_password_change_url(self):
        self.assertURLEqual(reverse("users:password_change"), "/password_change/")

    def test_password_change_done_url(self):
        self.assertURLEqual(reverse("users:password_change_done"), "/password_change/done/")

    def test_password_reset_url(self):
        self.assertURLEqual(reverse("users:password_reset"), "/password_reset/")

    def test_password_reset_done_url(self):
        self.assertURLEqual(reverse("users:password_reset_done"), "/password_reset/done/")

    def test_password_reset_confirm_url(self):
        self.assertURLEqual(
            reverse("users:password_reset_confirm", kwargs={"uidb64": "dummy_uidb64", "token": "dummy_token"}),
            "/reset/dummy_uidb64/dummy_token/",
        )

    def test_password_reset_complete_url(self):
        self.assertURLEqual(reverse("users:password_reset_complete"), "/reset/done/")

    def test_register_url(self):
        self.assertURLEqual(reverse("users:register"), "/register/")

    def test_mypage_url(self):
        self.assertURLEqual(reverse("users:mypage"), "/settings/account/")

    def test_email_update_url(self):
        self.assertURLEqual(reverse("users:email_update"), "/settings/account/email_update/")

    def test_account_update_url(self):
        self.assertURLEqual(reverse("users:account_update"), "/settings/account/update/")

    def test_account_delete_url(self):
        self.assertURLEqual(reverse("users:account_delete"), "/settings/account/delete/")

    def test_account_delete_complete_url(self):
        self.assertURLEqual(reverse("users:account_delete_complete"), "/settings/account/delete/done/")

    def test_user_detail_url(self):
        uuid = "c9403065-10d8-4e3b-bb7c-b2f7b235a8a3"
        self.assertURLEqual(reverse("users:user_detail", kwargs={"pk": uuid}), f"/user/{uuid}/")
