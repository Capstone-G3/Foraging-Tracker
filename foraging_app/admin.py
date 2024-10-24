from django.contrib import admin

from foraging_app.models.user import User, User_Profile
from foraging_app.models.group import Group
from foraging_app.models.marker import Marker
from foraging_app.models.species import Species

admin.site.register(User)
admin.site.register(Marker)
admin.site.register(Group)
admin.site.register(Species)
admin.site.register(User_Profile)
