from django.shortcuts import render, redirect
from django.views import View
from foraging_app.forms import UserRegistrationForm, UserProfileForm

class Register_View(View):
    def get(self, request):
        user_form = UserRegistrationForm()
        profile_form = UserProfileForm()
        return render(request, 'users/register.html', {'user_form': user_form, 'profile_form': profile_form})

    def post(self, request):
        user_form = UserRegistrationForm(request.POST, request.FILES)
        profile_form = UserProfileForm(request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save(commit=False)
            user.set_password(user_form.cleaned_data['password'])
            user.save()

            profile = profile_form.save(commit=False)
            profile.user_id = user
            profile.save()

            return redirect('login')  # Redirect to a login page after successful registration
        else:
            print(user_form.errors, profile_form.errors) #debugging
        return render(request, 'users/register.html', {'user_form': user_form, 'profile_form': profile_form})
