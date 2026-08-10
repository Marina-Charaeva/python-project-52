from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib import messages
from django.urls import reverse_lazy

class IndexView(TemplateView):
    template_name = 'index.html'

class UserListView(ListView):
    model = User
    template_name = 'users.html'
    context_object_name = 'users'
    ordering = ['id']

class UserCreateView(CreateView):
    form_class = UserCreationForm
    template_name = 'registration/register.html'
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, 'Пользователь успешно зарегистрирован')
        return response

class UserUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    fields = ['first_name', 'last_name', 'username']
    template_name = 'users/user_form.html'
    success_url = reverse_lazy('users')

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object.pk != request.user.pk:
            messages.error(request, 'У вас нет прав для изменения')
            return redirect('users')
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        messages.success(self.request, 'Пользователь успешно изменен')
        return super().form_valid(form)

class UserDeleteView(LoginRequiredMixin, DeleteView):
    model = User
    template_name = 'users/user_confirm_delete.html'
    success_url = reverse_lazy('users')

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object.pk != request.user.pk:
            messages.error(request, 'У вас нет прав для удаления')
            return redirect('users')
        return super().dispatch(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        response = super().delete(request, *args, **kwargs)
        messages.success(request, 'Пользователь успешно удален')
        return response