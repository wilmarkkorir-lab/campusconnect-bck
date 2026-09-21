from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from . import views

urlpatterns = [
    path('register/', views.RegisterView.as_view(), name='register'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('verify-email/', views.VerifyEmailView.as_view(), name='verify_email'),
    path('resend-otp/', views.ResendOTPView.as_view(), name='resend_otp'),
    path('forgot-password/', views.ForgotPasswordView.as_view(), name='forgot_password'),
    path('reset-password/', views.ResetPasswordView.as_view(), name='reset_password'),
    path('change-password/', views.ChangePasswordView.as_view(), name='change_password'),
    path('2fa/setup/', views.TwoFactorSetupView.as_view(), name='2fa_setup'),
    path('me/', views.MeView.as_view(), name='me'),
    path('profile/student/', views.StudentProfileView.as_view(), name='student_profile'),
    path('profile/lecturer/', views.LecturerProfileView.as_view(), name='lecturer_profile'),
    path('profile/leader/', views.StudentLeaderProfileView.as_view(), name='leader_profile'),
    path('profile/classrep/', views.ClassRepProfileView.as_view(), name='classrep_profile'),
    path('leaders/', views.StudentLeaderListView.as_view(), name='leader_list'),
    path('login-history/', views.LoginHistoryView.as_view(), name='login_history'),
    path('block/<uuid:user_id>/', views.BlockUserView.as_view(), name='block_user'),
    path('blocked/', views.BlockedUsersListView.as_view(), name='blocked_users'),
    # Admin
    path('users/', views.UserListView.as_view(), name='user_list'),
    path('users/<uuid:pk>/', views.UserDetailView.as_view(), name='user_detail'),
]
