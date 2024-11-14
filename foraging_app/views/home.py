from django.views import View
from django.shortcuts import render, reverse, redirect, get_object_or_404
from forage.sitemap import DesktopMap, BaseMap
from foraging_app.forms import CommentForm
from foraging_app.models import Marker, Species, Group
from foraging_app.models.group import User_Group
from foraging_app.models.user import User_Profile, User
from foraging_app.models.friend import Friend
from django.contrib import messages


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
        group_filter = request.GET.getlist('group')
        user_query = request.GET.get('q')
        profile_query = request.GET.get('u')
        group_query = request.GET.get('g')
        friend_filter = request.GET.getlist('friend')

        if profile_query:
            print("profile query")
            profiles = User_Profile.objects.filter(user_id__username__icontains=profile_query)
            print(profiles)
            markers = None
            groups = None

        elif group_query:
            groups = Group.objects.filter(name__icontains=group_query)
            markers = None
            profiles = None

        else:
            markers = Marker.objects.filter(is_private=False).order_by('-created_date')

            if species_filter:
                markers = markers.filter(species__name__in=species_filter)

            if user_query:
                markers = markers.filter(owner__username__icontains=user_query)

            if group_filter:
                print(f"Filtering markers by group: {group_filter}")

                # Find all users in the specified groups
                user_ids_in_groups = User_Group.objects.filter(group_id__name__in=group_filter).values_list('user_id',
                                                                                                            flat=True)

                # Filter markers by the users found in the groups
                markers = markers.filter(owner__id__in=user_ids_in_groups)
            if friend_filter:
                print(f"Filtering markers by friends: {friend_filter}")

                friends = User.objects.filter(username__in=friend_filter)


                markers = Marker.objects.filter(owner__in=friends)

            profiles = None
            groups = None
            print(request.user.getGroups())

        species_list = Species.objects.all()
        user_groups = Group.objects.filter(isPrivate=False)
        friends = Friend.objects.filter(friends=request.user)

        return render(request, 'feed.html', {
            'markers': markers,
            'species_filter': species_filter,
            'group_filter': group_filter,
            'friend_filter': friend_filter,
            'species_list': species_list,
            'profiles': profiles,
            'groups': groups,
            'user_groups': user_groups,
            'form': CommentForm(),
            'friends': friends
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

class ShareMarkerView(View):
    def post(self, request, *args, **kwargs):
        marker_id = request.POST.get('marker_id')
        friend_id = request.POST.get('friend_id')
        # Try to fetch the marker and friend, and handle errors
        try:
            marker = get_object_or_404(Marker, id=marker_id)
            friend = get_object_or_404(Friend, user_id=friend_id)

            # Add the marker to friend's shared markers list
            friend.shared_markers.add(marker)

            # Add a success message
            messages.success(request, 'Marker shared successfully')
        except Exception as e:
            # Add an error message if something goes wrong
            messages.error(request, 'Failed to share marker: ' + str(e))
        return redirect('feed')