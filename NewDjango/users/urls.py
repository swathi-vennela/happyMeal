from django.conf.urls import url
from django.contrib.auth import views as auth_views
from django.urls import path
from . import views
from users.forms import MyAuthForm, PasswordResetFormCustom

app_name = 'users'

urlpatterns = [
    path('profile/', views.profile, name='profile'),
    url(r'^signup/$', views.student_signup, name='signup'),
    url(r'^signupstore/$', views.store_signup, name='signupstore'),

    url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        views.activate, name='activate'),
    path('login/', auth_views.LoginView.as_view(template_name='users/login.html', authentication_form=MyAuthForm),
         name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='users/logout.html'), name='logout'),
    url(r'^change-password/$', views.change_password, name='change_password'),
    path('password-reset/',
         auth_views.PasswordResetView.as_view(
             template_name='users/password_reset.html', form_class=PasswordResetFormCustom
         ),
         name='password_reset'),
    url(r'^UserFeedback/$',views.UserFeedback,name='UserFeedback')
    # path('password-reset/done/',
    #      auth_views.PasswordResetDoneView.as_view(
    #          template_name='users/password_reset_done.html'
    #      ),
    #      name='password_reset_done'),
    # path('password-reset-confirm/<uidb64>/<token>/',
    #      auth_views.PasswordResetConfirmView.as_view(
    #          template_name='users/password_reset_confirm.html'
    #      ),
    #      name='password_reset_confirm'),
    # path('password-reset-complete/',
    #      auth_views.PasswordResetCompleteView.as_view(
    #          template_name='users/password_reset_complete.html'
    #      ),
    #      name='password_reset_complete'),

]
