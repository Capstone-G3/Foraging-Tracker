from django.forms import ModelForm
from foraging_app.models import Group, User

class GroupCreateForm(ModelForm):
    class Meta:
        model = Group
        fields = ['name',
                  'isPrivate',
                  'description']
