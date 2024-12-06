from django.db.models.signals import post_save, post_delete
from django.contrib.auth.signals import user_logged_in
from datetime import datetime
import pytz
from django.dispatch import receiver
from foraging_app.models.marker import Like_Marker, Comment, Marker
from foraging_app.models.user import User

@receiver(post_save, sender=Like_Marker)
def reward_on_likes(sender,instance,created, **kwargs):
    if created:
        marker = instance.marker_id
        if Like_Marker.objects.filter(marker_id=marker).count() == 5:
            marker.owner.rating += 10
            marker.owner.save()

@receiver(post_delete, sender=Like_Marker)
def adjust_on_unlike(sender, instance, **kwargs):
    marker = instance.marker_id
    if Like_Marker.objects.filter(marker_id=marker).count() < 5:
        print("less than 5")
        marker.owner.rating -=10
        marker.owner.save()


@receiver(post_save, sender=Like_Marker)
def add_point_on_like(sender, instance, created, **kwargs):
    if created:
        user = instance.user_id
        user.rating += 1  # Add one point to the user's rating for liking a post
        user.save()

@receiver(post_delete, sender=Like_Marker)
def remove_point_on_unlike(sender, instance, **kwargs):
    user = instance.user_id
    user.rating -= 1  # Remove one point from the user's rating for unliking a post
    user.save()

@receiver(post_save, sender=Comment)
def add_point_on_comment(sender, instance, created, **kwargs):
    if created:
        user = instance.user
        user.rating += 2  # Add one point to the user's rating for commenting on a post
        user.save()

@receiver(post_delete, sender=Comment)
def remove_point_on_comment_delete(sender, instance, **kwargs):
    user = instance.user
    user.rating -= 2  # Remove one point from the user's rating for deleting a comment
    user.save()

@receiver(user_logged_in)
def daily_login_reward(sender, request, user, **kwargs):
    last_login = user.last_login
    local_tz = pytz.timezone('America/Chicago')  # Replace with your local time zone
    now = datetime.now(pytz.utc).astimezone(local_tz)
    today = now.date()

    if last_login:
        last_login_date = last_login.astimezone(local_tz).date()
    else:
        last_login_date = None

    print(f"Last login (local): {last_login_date}, Today (local): {today}")  # Debugging output

    # Check if the user has logged in today
    if not last_login_date or last_login_date < today:
        user.rating += 1  # Award one point for daily login
        user.save()
        print(f"Awarded 1 point to {user.username}, new rating: {user.rating}")  # Debugging output
    else:
        print(f"No points awarded to {user.username}, already logged in today")  # Debugging output


