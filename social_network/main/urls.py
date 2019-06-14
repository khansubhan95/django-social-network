from django.urls import path, re_path, include
from django.contrib.auth.views import PasswordResetView, PasswordResetConfirmView
from . import views

app_name = 'main'

urlpatterns = [
    path('', views.homepage, name="homepage"),
    path('login/', views.login_request, name="login"),
    path('logout/', views.logout_request, name="logout"),
    path('register/', views.register_request, name="register"),
    path('profile/', views.profile_request, name="profile"),
    path('myposts/', views.user_posts, name="myposts"),
    path('posts/<int:post_id>/', views.detail, name='detail'),
    path('posts/edit/<int:post_id>/', views.edit, name='edit'),
    path('users/<int:user_id>', views.view_user, name="user_detail"),
    re_path('activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/',views.activate, name='activate'),
    path('posts/delete/<int:post_id>/', views.delete, name='delete'),
    path('forgot-password/', views.forgot_password, name='forgot_password'),
    re_path('reset-password/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/', views.reset_password, name='reset_password'),

]
