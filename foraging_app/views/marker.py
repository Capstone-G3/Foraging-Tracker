from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.contrib import messages
from django.urls import reverse

from foraging_app.forms import MarkerCreateForm, MarkerEditForm
from foraging_app.models import Species, Marker,Like_Marker, User

class Marker_Home_View(LoginRequiredMixin, View):
    login_url = '/login/'
    redirect_field_name = 'login'

    def get(self,request):
        user = None
        if request.user is not None and request.user.is_authenticated:
            user = request.user
        else:
            return redirect('/')

        markers = list(Marker.objects.filter(owner=user))
        print(markers)
        return render(
            request,
            'markers/home.html',
            {'marker_list' : markers}
        )

class Marker_Create_View(LoginRequiredMixin, View):
    login_url = '/login/'
    redirect_field_name = 'login'
    permission_denied_message = "Please Login Before Access"
    
    def getCreateForm(self):
        species = list(Species.objects.all())
        return MarkerCreateForm(initial={'species' : species})

    def get(self,request):
        form = self.getCreateForm()
        return render(request, 'markers/create.html', {'form' : form })
    
    def post(self,request):
        form = MarkerCreateForm(request.POST, request.FILES)
        status = 400
        if form.is_valid():
            data = form.cleaned_data
            # TODO : Resize Image before save -> Save space.
            marker_create = Marker.objects.create(**data, owner=request.user)
            if marker_create is not None:
                messages.success(request,"Marker created complete.")
                return redirect('/', permanent=True)
        else:
            messages.error(request, "Marker failed to create.")
        return render(
            request,
            'markers/create.html',
            {
                'form' : self.getCreateForm()
            },
            status=status
        )
    
class Marker_Edit_View(LoginRequiredMixin, View):
    login_url = '/login/'
    redirect_field_name = 'login'

    def get(self, request, marker_id):
        # The Marker exist.
        query = Marker.objects.get(id=marker_id)
        if query is None:
            messages.error(request,'Marker does not exist.')
            return redirect('/') # 404 Later.
        
        # Double Guard making sure User owned the following marker.
        if (request.user is not None) and (request.user.is_authenticated):
            list_owned = Marker.objects.filter(owner=request.user)
            if query not in list_owned:
                messages.error(request, "The following marker is not owned by you.")
                return redirect('/') # 401 Later.
        
        form = MarkerEditForm(instance=query)
        return render(request, 'markers/edit.html', {'form' : form, 'marker' : query})
    
    def post(self,request, marker_id):
        status = 404
        query = Marker.objects.get(id=marker_id)
        form = MarkerEditForm(request.POST, request.FILES, instance=query)
        if form.is_valid():
            form.save(commit=True)
            messages.success(request,"Marker edited successfully.")
            url = reverse('info_marker', kwargs={'marker_id': marker_id})
            return redirect(url) # 301
        else:
            messages.error(request,"Edit marker failed.")
        return render(
            request,
            'markers/edit.html',
            {
                'form' : MarkerEditForm(instance=query),
            },
            status=status
        )

class Marker_Delete_View(LoginRequiredMixin, View):
    login_url = '/login/'
    redirect_field_name = 'login'

    def get(self,request,marker_id):
        return Marker_Edit_View().get(request,marker_id)

    def post(self,request,marker_id):
        if request.user is None or not request.user.is_authenticated:
            return redirect('/') # 401
        query = Marker.objects.get(id=marker_id)
        if query is None:
            return redirect('/') # 404
        query.delete()
        messages.success(request,'Marker removed complete.')
        return redirect('home_marker')

class Marker_Details_View(LoginRequiredMixin, View):
    def get(self,request,marker_id):
        query = Marker.objects.get(id=marker_id)
        query_likes = Like_Marker.objects.filter(marker_id=marker_id)
        users = []
        if not query_likes:
            pass

        for user_like in query_likes:
            user = User.objects.get(id=user_like.id)
            if not user :
                continue
            users.append(user)
        
        data = {
            'title' : query.title,
            'owner_name' : "@" + str(query.owner.username),
            'latitude' : query.latitude,
            'longitutde' : query.longitude,
            'description' : query.description,
            'species' : query.species,
            'found' : query.created_date,
            'image' : query.image.url
        }

        return render(request,'markers/info.html',{
            'marker' : data.items(),
            'owner' : query.owner,
            'users_like': users[0:3],
            'total_likes' : len(users),
            'url_resolve' : marker_id
            }
        )