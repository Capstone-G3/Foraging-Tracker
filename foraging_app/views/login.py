from django.views import View
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.core.mail import send_mail
from django.urls import reverse_lazy
from django.contrib.auth.views import PasswordResetView
from django.contrib.messages.views import SuccessMessageMixin


class Login_View(View):
    #def __init__(self):
     #   self.figure = sitemap.getDefaultMap()
    def get(self,request):
        return render(request, "login.html", {})
    
    def post(self,request):
        #take what is posted from form and assigning to username and password
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        
        #return redirect('home')
    
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.success(request, ("Username or Password Do Not Match, Try Again..."))
            return redirect('login')

def send_email_view(request):
    if request.method == 'POST':
        send_mail(
        'test',
        'test',
        'foraging.tracker@outlook.com',
        ['jennifer.justus7@gmail.com'],
        fail_silently=False,
        )
        return redirect('login')
    return redirect('home')
class ResetPasswordView(SuccessMessageMixin, PasswordResetView):
    template_name = 'users/password_reset.html'
    email_template_name = 'users/password_reset_email.html'
    subject_template_name = 'users/password_reset_subject.txt'
    success_message = "We've emailed you instructions for setting your password, " \
                      "if an account exists with the email you entered. You should receive them shortly." \
                      " If you don't receive an email, " \
                      "please make sure you've entered the address you registered with, and check your spam folder."
    
    success_url = reverse_lazy('home') 
