"""stackoverflow URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.conf.urls import url
from django.contrib import admin
from django.urls import path,include
from questions import views
from stackoverflow import settings
from django.conf.urls.static import static
from stackoverflow.errorview import errorView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('feed/', views.get_feed, name='feed'),
    path('', views.get_feed),
    path('question/', include("questions.urls")),
    # url(r'^user.?/', include("users.urls")),
    path('user/', include("users.urls")),
    url(r'^.*$', errorView, name='catch-all'),
]


urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)