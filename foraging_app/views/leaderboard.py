from django.views import View
from django.shortcuts import render
from foraging_app.models import User
from foraging_app.models.friend import Friend


class LeaderboardView(View):
    def get(self, request):
        view_type = request.GET.get('view', 'all_time')  # Default to 'all_time'
        template_name = 'leaderboard.html'

        if view_type == 'friends':
            try:
                user_friends = Friend.objects.get(user=request.user).friends.all()
            except Friend.DoesNotExist:
                user_friends = None

            if user_friends:
                users = list(user_friends) + [request.user]
                queryset = User.objects.filter(username__in=[user.username for user in users]).order_by('-rating')[:10]
            else:
                queryset = None
        else:
            queryset = User.objects.order_by('-rating')[:10]  # Top 10 users based on rating

        return render(request, template_name, {'users': queryset, 'view_type': view_type})



