from django.contrib.auth import logout, authenticate
from django.core.checks import messages
from django.shortcuts import redirect, render
from django.views import View
from django.contrib import messages


class Logout_View(View):
    def get(self, request):
        return render(request, "logout.html")
    def post(self, request):
        logout(request)
        messages.success(request, "You have been logged out.")
        return redirect('home')
