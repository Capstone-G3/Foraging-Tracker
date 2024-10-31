from django.views import View
from django.shortcuts import render, reverse, redirect
from forage.sitemap import DesktopMap, BaseMap
from foraging_app.forms import CommentForm
from foraging_app.models import Marker, Species

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
        marker_id = request.GET.get('marker_id')
        highlighted_marker = None

        for marker in self.list_contents:
            home_map.add_marker(location=marker['location'], contents=marker['contents'])
            if marker_id and marker['contents']['marker_ref'].endswith(f"/{marker_id}/"):
                highlighted_marker = marker
        print(highlighted_marker)
        if highlighted_marker:
            home_map.set_center(highlighted_marker['location'])

        username = request.user.username if request.user.is_authenticated else "Log In"
        return render(request, "map.html", {
            "map": home_map.compile_figure(),
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