from django.views import View
from django.shortcuts import render, reverse, redirect, get_object_or_404
from forage.sitemap import DesktopMap, BaseMap
from foraging_app.forms import CommentForm
from foraging_app.models import Marker, Species
from foraging_app.models.user import User_Profile


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


        for marker in self.list_contents:
            home_map.add_marker(location=marker['location'], contents=marker['contents'])

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
        profile_query = request.GET.get('u')
        print(profile_query)
        if profile_query:
            print("profile query")
            profiles = User_Profile.objects.filter(user_id__username__icontains=profile_query)
            print(profiles)
            markers = None

        else:
            markers = Marker.objects.filter(is_private=False).order_by('-created_date')

            if species_filter:
                markers = markers.filter(species__name__in=species_filter)

            if user_query:
                markers = markers.filter(owner__username__icontains=user_query)
            profiles = None
        species_list = Species.objects.all()
        print(markers)
        return render(request, 'feed.html', {
            'markers': markers,
            'species_filter': species_filter,
            'species_list': species_list,
            'profiles': profiles,
            'form': CommentForm()
        })

class AddCommentView(View):
    def post(self, request, marker_id):
        #current_url = request.build_absolute_uri()
        #print(current_url)
        marker = Marker.objects.get(id=marker_id)
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.marker = marker
            comment.user = request.user
            comment.save()
        return redirect('feed')

class SingleMarkerView(View):
    def get(self, request, marker_id):
        print(marker_id)
        marker = get_object_or_404(Marker, id=marker_id)
        home_map = BaseMap()  # Instantiate BaseMap without center_location
        home_map.__map__.location = [marker.latitude, marker.longitude]  # Center map on the marker's coordinates
        home_map.__map__.zoom_start = 18
        category = marker.species.category if marker.species else ''
        # Add the marker to the map
        home_map.add_marker(
            location=(marker.latitude, marker.longitude),
            contents= {
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

        )
        return render(request, "single_marker_map.html", {
            "map": home_map.compile_figure(),
        })
