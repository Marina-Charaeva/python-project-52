from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, TemplateView, View  # <--- ДОБАВЛЕНО: View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout
from django.contrib import messages
from django.urls import reverse_lazy
from .forms import CustomAuthenticationForm, CustomUserCreationForm


class IndexView(TemplateView):
    template_name = 'index.html'


class UserListView(ListView):
    model = User
    template_name = 'users/users.html'
    context_object_name = 'users'
    ordering = ['id']


class UserCreateView(SuccessMessageMixin, CreateView):
    model = User
    form_class = CustomUserCreationForm
    template_name = 'users/create.html'
    success_url = reverse_lazy('login')
    success_message = 'Пользователь успешно зарегистрирован'


class UserLoginView(View):
    template_name = 'users/login.html'
    
    def get(self, request):
        if request.user.is_authenticated:
            return redirect('index')
        form = CustomAuthenticationForm()
        return render(request, self.template_name, {'form': form})
    
    def post(self, request):
        form = CustomAuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, 'Вы залогинены')
            return redirect('index')
        return render(request, self.template_name, {'form': form})

class UserLogoutView(View):
    def post(self, request):
        logout(request)
        messages.info(request, 'Вы разлогинены')
        return redirect('index')

class UserUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView)):
    model = User
    fields = ['first_name', 'last_name', 'username']
    template_name = 'users/update.html'
    success_url = reverse_lazy('users')
    success_message = 'Пользователь успешно изменен'

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        # Разрешаем редактировать только себя
        if self.object.pk != request.user.pk:
            messages.error(request, 'У вас нет прав для изменения другого пользователя')
            return redirect('users')
        return super().dispatch(request, *args, **kwargs)

class UserDeleteView(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = User
    template_name = 'users/delete.html'
    success_url = reverse_lazy('users')
    success_message = 'Пользователь успешно удален'

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        # Разрешаем удалять только себя
        if self.object.pk != request.user.pk:
            messages.error(request, 'У вас нет прав для удаления другого пользователя')
            return redirect('users')
        return super().dispatch(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        response = super().delete(request, *args, **kwargs)
        messages.success(request, self.success_message)
        return response
