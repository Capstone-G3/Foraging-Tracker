"""
URL configuration for foraging_app project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path
from foraging_app.views.home import Home_View, About_Us_View
from foraging_app.views.login import Login_View
from foraging_app.views.logout import Logout_View
from foraging_app.views.registration import Register_View
from foraging_app.views.marker import Marker_Create_View, Marker_Edit_View, Marker_Home_View, Marker_Delete_View, Marker_Details_View
from foraging_app import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', Home_View.as_view(), name='home'),

    #Login urls
    path('login/', Login_View.as_view(), name='login'),
    path('password-reset/', auth_views.PasswordResetView.as_view(template_name='users/password_reset.html'), name='password-reset'),
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='users/password_reset_done.html'),name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='users/password_reset_confirm.html'),name='password_reset_confirm'),
    path('password-reset-complete/',auth_views.PasswordResetCompleteView.as_view(template_name='users/password_reset_complete.html',),name='password_reset_complete'),
    path('register/', Register_View.as_view(), name = 'register'),
    path('about_us/', About_Us_View.as_view(), name='about_us'),

    #Logout url
    path('logout/', Logout_View.as_view(), name="logout"),


    # Marker urls
    path('markers/', Marker_Home_View.as_view(), name='home_marker'),
    # TODO : Add dynamic marker for onsite form.
    path('marker/create', Marker_Create_View.as_view(), name="create_marker"),
    path('marker/<int:marker_id>', Marker_Details_View.as_view(), name='info_marker'),
    path('marker/<int:marker_id>/edit', Marker_Edit_View.as_view(), name='edit_marker'),
    path('marker/<int:marker_id>/edit/delete', Marker_Delete_View.as_view(), name='delete_marker'),
    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) # Remove for production.
