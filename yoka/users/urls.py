from django.urls import path
from django.views.generic import TemplateView

from . import views

app_name = "users"
urlpatterns = [
    # 認証系
    path("login/", views.LoginView.as_view(), name="login"),
    path("logout/", views.LogoutView.as_view(), name="logout"),
    path("password_change/", views.PasswordChangeView.as_view(), name="password_change"),
    path("password_change/done/", views.PasswordChangeDoneView.as_view(), name="password_change_done"),
    path("password_reset/", views.PasswordResetView.as_view(), name="password_reset"),
    path("password_reset/done/", views.PasswordResetDoneView.as_view(), name="password_reset_done"),
    path("reset/<uidb64>/<token>/", views.PasswordResetConfirmView.as_view(), name="password_reset_confirm"),
    path("reset/done/", views.PasswordResetCompleteView.as_view(), name="password_reset_complete"),
    path("register/", views.RegisterView.as_view(), name="register"),

    # 個人設定
    path("settings/account/", views.MyPageView.as_view(), name="mypage"),
    path("settings/account/email_update/", views.EmailUpdateView.as_view(), name="email_update"),
    path("settings/account/update/", views.AccountUpdateView.as_view(), name="account_update"),
    path("settings/account/delete/", views.AccountDeleteView.as_view(), name="account_delete"),
    path(
        "settings/account/delete/done/",
        TemplateView.as_view(template_name="users/delete_complete.html"),
        name="account_delete_complete",
    ),

    # プロフィールページ
    path("user/<uuid:pk>/", views.UserDetailView.as_view(), name="user_detail"),
]
