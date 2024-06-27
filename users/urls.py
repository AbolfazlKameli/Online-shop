from django.urls import path, include

from . import views

app_name = 'users'

password_reset = [
    path('', views.UserPasswordResetView.as_view(), name='user_password_reset'),
    path('done/', views.UserPasswordResetDoneView.as_view(), name='user_password_reset_done'),
    path('confirm/<uidb64>/<token>/', views.UserPasswordResetConfirmView.as_view(), name='user_password_reset_confirm'),
    path('complete/', views.UserPasswordResetCompleteView.as_view(), name='user_password_reset_complete'),
]

urlpatterns = [
    path('register/', views.UserRegisterView.as_view(), name='user_register'),
    path('login/', views.UserLoginView.as_view(), name='user_login'),
    path('logout/', views.UserLogoutView.as_view(), name='user_logout'),
    path('register/verify_code/', views.UserRegisterVerifyView.as_view(), name='user_register_verify'),
    path('login/verify_code/', views.UserLoginVerifyView.as_view(), name='user_login_verify'),
    path('reset_password/', include(password_reset)),
    path('profile/', views.UserProfileView.as_view(), name='user_profile'),
    path('edit_profile/', views.UserProfileEditView.as_view(), name='edit_profile'),
]
