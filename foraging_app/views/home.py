from django.views import View
from django.shortcuts import render, reverse, redirect
from forage.sitemap import DesktopMap, BaseMap
from foraging_app.forms import CommentForm
from foraging_app.models import Marker, Species

class Home_View(View):
    def __init__(self):
        self.list_contents = []

    def getAllMarkers(self, request):
        query_marker = Marker.objects.all()
        for marker in query_marker:
            contents = {
                'marker' : marker,
                'owner' : marker.owner,
                'request' : request
            }
            self.list_contents.append(contents)

    # Complete.
    def get(self,request):
        username = request.user.username if request.user.is_authenticated else 'Log In'
        device  = request.user_agent
        home_map = DesktopMap()
        if (device.is_mobile or device.is_tablet) and device.is_touch_capable:
            home_map = BaseMap()
        self.getAllMarkers(request)
        for marker in self.list_contents:
            home_map.add_marker(
                location=(marker['marker'].latitude,marker['marker'].longitude),
                contents=marker
            )

        return render(
            request,
            "index.html",
            {
                "map" : home_map.compile_figure(),
                'username' : username
            }
        )

class About_Us_View(View):
    def get(self, request):
        return render(request, "about_us.html")

class NavBar_View(View):
    def get(self, request):
        return render(request, 'base.html')


class Feed_View(View):
    def get(self, request):
        species_filter = request.GET.getlist('species')
        user_query = request.GET.get('q')

        markers = Marker.objects.filter(is_private=False).order_by('-created_date')

        if species_filter:
            markers = markers.filter(species__name__in=species_filter)

        if user_query:
            markers = markers.filter(owner__username__icontains=user_query)

        species_list = Species.objects.all()

        return render(request, 'feed.html', {
            'markers': markers,
            'species_filter': species_filter,
            'species_list': species_list,
            'form': CommentForm()
        })

class AddCommentView(View):
    def post(self, request, marker_id):
        marker = Marker.objects.get(id=marker_id)
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.marker = marker
            comment.user = request.user
            comment.save()
        return redirect('feed')
