from django.contrib import admin
from django.contrib.auth import views
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from userprofile.forms import LoginForm
from core.views import index, about
 
urlpatterns = [
    path('admin/', admin.site.urls),
    path('dashboard/', include('userprofile.urls')),
    path('dashboard/leads/', include('lead.urls')),
    path('dashboard/', include('dashboard.urls')),
    path('dashboard/teams/', include('team.urls')),
    path('', index, name="index"),
    path('dashboard/clients/', include('client.urls')),
    path('about/', about, name="about"),
    path('log-in/', views.LoginView.as_view(template_name='userprofile/login.html', authentication_form=LoginForm), name="login"),
    path('log-out/', auth_views.LogoutView.as_view(), name="logout"),
    ]+static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
