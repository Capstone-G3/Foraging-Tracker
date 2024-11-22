from django.db.models import Model, ForeignKey, TextField, DateTimeField, BooleanField, CASCADE
from foraging_app.models.user import User
from foraging_app.models import Marker

class Notification(Model):
    user = ForeignKey(User, on_delete=CASCADE, related_name='notifications')
    marker = ForeignKey(Marker, on_delete=CASCADE, null=True, blank=True)
    message = TextField()
    created_at = DateTimeField(auto_now_add=True)
    is_read = BooleanField(default=False)


    def __str__(self):
        return f"Notification for {self.user} - {self.message}"
