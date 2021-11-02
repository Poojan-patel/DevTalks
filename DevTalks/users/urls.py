from django.urls import path
from django.conf.urls import url
from django.conf.urls.static import static
from django.conf import settings
from . import views

urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('signin/', views.signin, name='signin'),
    path('signout/', views.signout, name='signout'),
    path('profile/', views.profile, name='profile'),
    path('change-password/',views.change_password, name='change_password'),
    path('forgot-password/',views.forgot_password, name='forgot_password'),
    url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,40})/$',
        views.activate, name='activate'),
    path('check_username/<username>/',views.check_username, name='check_username'),
    path('check_email/<email>/',views.check_email, name='check_email'),
    path('', views.signin),
]

# if settings.DEBUG:
# 	urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


