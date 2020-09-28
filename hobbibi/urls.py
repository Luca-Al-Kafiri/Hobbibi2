from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('search', views.search, name='search'),
    path('profile/<str:user>', views.profile, name='profile'),
    path('add', views.add, name="add"),
    path('delete', views.delete, name="delete"),
    path('delete_msg', views.delete_msg, name="delete_msg"),
    path('message', views.message, name="message"),
    path('register', views.register, name="register"),
    path('login', views.login_view, name="login"),
    path('logout', views.logout_view, name="logout"),
]