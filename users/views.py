from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from django.contrib.auth import login, authenticate, update_session_auth_hash
from django.views.generic import CreateView
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin


class RegisterUser(CreateView):
    form_class = UserCreationForm

    def get(self, request, *args, **kwargs):
        return render(request, 'users/register-user.html', {'form': UserCreationForm()})

    def post(self, request, *args, **kwargs):
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, f'Welcome, {username}!')
            return redirect('cars')
        return render(request, 'users/register-user.html', {'form': form})


class ChangePassword(LoginRequiredMixin, CreateView):
    form_class = PasswordChangeForm

    def get(self, request, *args, **kwargs):
        form = PasswordChangeForm(request.user)
        return render(request, 'users/change-password.html', {'form': form})

    def post(self, request, *args, **kwargs):
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Password changed!')
            return redirect('cars')
        return render(request, 'users/change-password.html', {'form': form})
