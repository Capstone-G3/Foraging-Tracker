from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.views import View
from foraging_app.models.user import User_Profile


class EditProfileView(LoginRequiredMixin, View):
    def get(self, request):
        if not request.user.is_authenticated:
            return redirect('home')

        user = request.user
        print(user)
        print(user.profile_image)
        try:
            user_profile = User_Profile.objects.get(user_id=user)
        except User_Profile.DoesNotExist:
            user_profile = None
        if user_profile is None:
            return redirect('home')

        return render(request, 'edit_profile_form.html', {'user': user, 'user_profile': user_profile})

    def post(self, request):
        user = request.user
        profile = User_Profile.objects.get(user_id=request.user)

        user.first_name = request.POST['first_name']
        user.last_name = request.POST['last_name']
        user.email = request.POST['email']
        user.username = request.POST['username']

        profile.bio = request.POST['bio']
        profile.phone = request.POST['phone']
        profile.home_address = request.POST['address']


        if request.FILES.get('profile_image'):
            user.profile_image = request.FILES['profile_image']

        user.save()
        print(user.profile_image)
        profile.save()
        return redirect('home')
