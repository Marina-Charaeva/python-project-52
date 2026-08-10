from django.contrib import admin
from django.urls import path, include
from django.contrib.auth.views import LoginView, LogoutView
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('users/', views.users, name='users'),
    path('users/create/', views.UserCreateView.as_view(), name='user-create'),
    path('users/<int:pk>/update/', views.UserUpdateView.as_view(), name='user-update'),
    path('users/<int:pk>/delete/', views.UserDeleteView.as_view(), name='user-delete'),
    path('login/', LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', LogoutView.as_view(next_page='index'), name='logout'),
    path('register/', views.register, name='register'),
    path('i18n/', include('django.conf.urls.i18n')),
    path('admin/', admin.site.urls),
]