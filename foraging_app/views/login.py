from django.views import View
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages

class Login_View(View):

    def get(self, request):
        return render(request, "login.html", {})

    def post(self, request):
        # take what is posted from form and assigning to username and password
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.success(request, ("Username or Password Do Not Match, Try Again..."))
            return redirect('login')
