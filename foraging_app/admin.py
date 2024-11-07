from django.contrib import admin

from foraging_app.models.user import User
from foraging_app.models.group import Group
from foraging_app.models.marker import Marker
from foraging_app.models.species import Species
from foraging_app.models.friend import Friend, Friend_Request

admin.site.register(User)
admin.site.register(Marker)
admin.site.register(Group)
admin.site.register(Species)
admin.site.register(Friend)
admin.site.register(Friend_Request)

