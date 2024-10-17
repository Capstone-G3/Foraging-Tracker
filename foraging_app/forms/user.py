from django import forms
from foraging_app.models.user import User, User_Profile
from django.contrib.auth.password_validation import validate_password
import re
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth import get_user_model

#User = get_user_model()

class CustomPasswordResetForm(PasswordResetForm):
    def get_users(self, email):

        try:
            user_profile = User_Profile.objects.filter(email=email, user__is_active=True)
            print(user_profile.user_id)
            return [user_profile.user_id]
        except User_Profile.DoesNotExist:
            return []
    '''
    def get_users(self, email):
        user_profiles = User_Profile.objects.filter(email=email)
        for profile in user_profiles:
            yield profile.user_id
    '''
class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, min_length=8)
    confirm_password = forms.CharField(widget=forms.PasswordInput)
    email = forms.EmailField()
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'password', 'confirm_password', 'email']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")

        confirm_password = cleaned_data.get("confirm_password")

        if password is None:
            self.add_error('password',"Password cannot be empty")
            return cleaned_data
        if password != confirm_password:
            raise forms.ValidationError("Passwords do not match")

        # Validate the password strength
        try:
            validate_password(password)
        except forms.ValidationError as e:
            self.add_error('password', e)

        return cleaned_data

class UserProfileForm(forms.ModelForm):
    gender = forms.ChoiceField(choices=User_Profile.GENDER)

    class Meta:
        model = User_Profile
        fields = ['home_address', 'phone', 'gender']

    def clean_gender(self):
        gender = self.cleaned_data.get('gender')
        print(f"Gender value: {gender}")  # Debugging line
        valid_choices = [str(choice[0]) for choice in User_Profile.GENDER]
        if gender not in valid_choices:
            raise forms.ValidationError("Select a valid choice.")
        return gender

    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        if not re.match(r'^\d{10}$', phone):
            raise forms.ValidationError("Enter a valid 10-digit phone number.")
        return phone