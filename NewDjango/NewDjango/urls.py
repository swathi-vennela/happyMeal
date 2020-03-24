from django.contrib import admin
from django.urls import path, include
from blog import views as blog_views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('users.urls',namespace='users')),
    path('', blog_views.home, name='home'),
    path('about/', blog_views.about, name='about'),
    path('',include('core.urls',namespace='core',)),
    #path('menu/', blog_views.menu, name='menu'),
    path('contact/', blog_views.contact, name='contact'),


]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
