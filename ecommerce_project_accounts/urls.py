from django.urls import path
from .views import (
    login_page,
    custom_logout,
    register_page,
    profile_section,
    profile_update,
    password_update,
    activate_email,
    add_address,
    forget_password, verify_otp, new_password
)

app_name = 'accounts'

urlpatterns = [
    path('login/', login_page, name='login'),
    path('logout/', custom_logout, name='logout'),
    path('register/', register_page, name='register'),
    path('activate/<email_token>/', activate_email, name='activate_email'),
    path('profile_section/', profile_section, name='profile_section'),
    path('profile_update/', profile_update, name='profile_update'),
    path('password_update/', password_update, name='password_update'),
    path('add_address/', add_address, name='add_address'),
    path('forget-password/', forget_password, name='forget_password'),
    path('verify-otp/', verify_otp, name='verify_otp'),
    path('new-password/', new_password, name='new_password'),

]
