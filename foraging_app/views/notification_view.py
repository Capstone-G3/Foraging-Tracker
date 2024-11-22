from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, get_object_or_404
from django.views.generic import ListView
from foraging_app.models.notification import Notification
import pytz
from django.utils import timezone

class NotificationListView(ListView):
    model = Notification
    template_name = 'notification.html'
    context_object_name = 'notifications'

    def get_queryset(self):
        # Get all notifications and order by created_at descending
        notifications = self.request.user.notifications.all().order_by('-created_at')

        # Convert created_at to UTC
        utc_timezone = pytz.UTC
        for notification in notifications:
            notification.created_at = timezone.localtime(notification.created_at, utc_timezone)

        return notifications

@login_required
def mark_notifications_as_read(request):
    print("read")
    notifications = Notification.objects.filter(user=request.user, is_read=False)
    notifications.update(is_read=True)
    return redirect('notifications')

@login_required
def mark_notification_as_read(request, notification_id):
    notification = get_object_or_404(Notification, id=notification_id, user=request.user)
    notification.is_read = True
    notification.save()
    return redirect('notifications')  # Redirect to the notifications page
