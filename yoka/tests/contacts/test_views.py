from unittest.mock import patch

from django.test import TestCase
from django.urls import reverse


class TestContactCreateView(TestCase):

    def setUp(self):
        self.viewname = "contacts:contact_form"

    def test_simple_get(self):
        res = self.client.get(reverse(self.viewname))
        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, "contacts/contact_form.html")

    def test_post_confirm(self):
        """
        入力確認postのチェック
        """
        data = {
            "email": "test@example.com",
            "subject": "テストタイトル",
            "message": "テスト本文",
            "next": "confirm",
        }
        res = self.client.post(reverse(self.viewname), data)
        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, "contacts/contact_confirm.html")

    def test_post_back(self):
        """
        入力確認画面から戻るボタンをクリックした時のテスト
        """
        data = {
            "email": "test@example.com",
            "subject": "テストタイトル",
            "message": "テスト本文",
            "next":  "back",
        }
        res = self.client.post(reverse(self.viewname), data)
        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, "contacts/contact_form.html")

    def test_post_submit(self):
        """
        入力確認画面から送信ボタンをクリックした時のテスト
        """
        data = {
            "email": "test@example.com",
            "subject": "テストタイトル",
            "message": "テスト本文",
            "next":  "submit",
        }
        res = self.client.post(reverse(self.viewname), data)
        self.assertRedirects(res, reverse("contacts:contact_done"))

    @patch('yoka.contacts.signals.contact_done.send')
    def test_signal(self, mock):
        """
        シグナルによるメール送信テスト
        """
        data = {
            "email": "test@example.com",
            "subject": "テストタイトル",
            "message": "テスト本文",
            "next":  "submit",
        }
        self.client.post(reverse(self.viewname), data)
        self.assertTrue(mock.called)
        self.assertEqual(mock.call_count, 1)


class TestContactDoneView(TestCase):

    def setUp(self):
        self.url_name = "contacts:contact_done"

    def test_simple_get(self):
        res = self.client.get(reverse(self.url_name))
        self.assertEqual(res.status_code, 200)
        self.assertTemplateUsed(res, "contacts/contact_done.html")
