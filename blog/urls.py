from django.urls import path

from . import views

urlpatterns = [
path('homepage/', views.index, name='index'),
path('blog/', views.blog, name='blog'),
path('blog/posts/<int:post_id>', views.post, name='post'),
path('login/', views.login_view, name='login'),
path('logout/', views.logout_view, name='logout'),
path('epilepsy-test/', views.epilepsytest_view, name='epilepsytest'),
path('forum/', views.forum_view, name='forum'),
path('forum/threads/<int:thread_id>', views.thread, name='thread'),
path('register/', views.register_view, name='register'),
path('profile/<str:username>/', views.profile, name='profile'),
path('activate/<uidb64>/<token>/', views.activate, name='activate'),
path('account_activation_sent/', views.account_activation_sent, name='account_activation_sent'),
path('password_reset/', views.password_reset, name='password_reset'),
path('password_reset_done/', views.password_reset_done, name='password_reset_done'),
path('password_reset_confirm/<uidb64>/<token>/', views.password_reset_confirm, name='password_reset_confirm'),
]