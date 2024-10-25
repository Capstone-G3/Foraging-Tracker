from django.views import View
from django.shortcuts import render, reverse
from forage.sitemap import DesktopMap, BaseMap
from foraging_app.models import Marker

class Home_View(View):
    def __init__(self):
        self.list_contents = []

    def getAllMarkers(self):
        query_marker = Marker.objects.all()
        for marker in query_marker:
            category = marker.species.category if marker.species else ''
            contents = {
                'location': (marker.latitude, marker.longitude),
                'contents': {
                    'image_url': marker.image.url if marker.image and marker.image.name else '',
                    'species_name': marker.title.split(' ')[0],
                    'species_full_name': marker.title,
                    'latitude': str(marker.latitude),
                    'longitude': str(marker.longitude),
                    'category': str(category),
                    'description': str(marker.description),
                    'marker_ref': reverse('edit_marker', kwargs={'marker_id': marker.id}),
                    'marker_name': 'Edit ' + str(marker.title)
                }
            }
            self.list_contents.append(contents)

    def get(self, request):
        device = request.user_agent
        home_map = DesktopMap() if not (device.is_mobile or device.is_tablet) else BaseMap()
        self.getAllMarkers()
        for marker in self.list_contents:
            home_map.add_marker(location=marker['location'], contents=marker['contents'])
        username = request.user.username if request.user.is_authenticated else "Log In"
        return render(request, "index.html", {
            "map": home_map.compile_figure(),
            "markers": Marker.objects.filter(is_private=False).order_by('-created_date'),
            "username": username
        })

class About_Us_View(View):
    def get(self, request):
        return render(request, "about_us.html")

class NavBar_View(View):
    def get(self, request):
        return render(request, 'base.html')

class Feed_View(View):
    def get(self, request):
        markers = Marker.objects.filter(is_private=False).order_by('-created_date')
        return render(request, 'feed.html', {'markers': markers})