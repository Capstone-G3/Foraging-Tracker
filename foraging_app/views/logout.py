from django.contrib.auth import logout, authenticate
from django.core.checks import messages
from django.shortcuts import redirect, render
from django.views import View
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin


class Logout_View(LoginRequiredMixin ,View):
    login_url = '/login/'
    redirect_field_name = 'login'
    
    def post(self, request):
        logout(request)
        return redirect('home')
