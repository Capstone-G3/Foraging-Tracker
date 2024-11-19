from django.views import View
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from foraging_app.models import Marker, Like_Marker

@method_decorator(login_required, name='dispatch')
class LikeMarkerView(View):
    def post(self, request, marker_id):
        marker = Marker.objects.get(id=marker_id)
        user = request.user
        like, created = Like_Marker.objects.get_or_create(user_id=user, marker_id=marker)
        if not created:
            like.delete()
            liked = False
        else:
            liked = True
        return JsonResponse({'liked': liked, 'likes_count': marker.like_marker_set.count()})
