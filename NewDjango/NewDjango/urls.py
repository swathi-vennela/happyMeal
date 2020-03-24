from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from blog import views as blog_views
from django.conf import settings
from django.conf.urls.static import static
from users.forms import MyAuthForm, PasswordResetFormCustom

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('users.urls',namespace='users')),
    path('login/', auth_views.LoginView.as_view(template_name='users/login.html', authentication_form=MyAuthForm),
     name='login'),
    path('password-reset/done/',
         auth_views.PasswordResetDoneView.as_view(
             template_name='users/password_reset_done.html'
         ),
         name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(
             template_name='users/password_reset_confirm.html'
         ),
         name='password_reset_confirm'),
    path('password-reset-complete/',
     auth_views.PasswordResetCompleteView.as_view(
         template_name='users/password_reset_complete.html'
     ),
     name='password_reset_complete'),
    path('', blog_views.home, name='home'),
    path('about/', blog_views.about, name='about'),
    path('',include('core.urls',namespace='core',)),
    #path('menu/', blog_views.menu, name='menu'),
    path('contact/', blog_views.contact, name='contact'),


]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
