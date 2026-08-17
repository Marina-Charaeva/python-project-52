from django.contrib import admin
from django.urls import path, include
from django.contrib.auth.views import LoginView, LogoutView
from . import views

urlpatterns = [
    # Главная
    path('', views.IndexView.as_view(), name='index'),
    
    # Пользователи
    path('users/', views.UserListView.as_view(), name='users'),
    path('users/create/', views.UserCreateView.as_view(), name='register'),  # ← ТОЛЬКО ОДИН РАЗ
    path('users/<int:pk>/update/', views.UserUpdateView.as_view(), name='user_update'),
    path('users/<int:pk>/delete/', views.UserDeleteView.as_view(), name='user_delete'),
    
    # Аутентификация
    path('login/', views.UserLoginView.as_view(), name='login'),
    path('logout/', views.UserLogoutView.as_view(), name='logout'),
    
    # I18n
    path('i18n/', include('django.conf.urls.i18n')),
    
    # Админ
    path('admin/', admin.site.urls),
]