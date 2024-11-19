from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.views import View
from foraging_app.models.user import User_Profile  # Import the User_Profile model

class DeleteUserView(LoginRequiredMixin, View):
    def post(self, request):
        user = request.user
        try:
            user_profile = User_Profile.objects.get(user_id=user)
            user_profile.delete()  # Delete user profile first
            user.delete()  # Then delete user
            return redirect('home')
        except User_Profile.DoesNotExist:
            print(f"User profile does not exist for user: {user}")
        except Exception as e:
            print(f"Error deleting user: {e}")
        return redirect('about_us')

