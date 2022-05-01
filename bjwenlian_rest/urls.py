"""bjwenlian_rest URL Configuration

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
from django.views.static import serve
from django.contrib import admin
from django.urls import path, include, re_path

from bjwenlian_rest.settings import MEDIA_ROOT, PRODUCTION

urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', include('Account.urls')),
    path('passage/', include('Passage.urls')),
    path('activity/', include('Activity.urls')),
    path('post/',include('Post.urls'))
]
if not PRODUCTION:
    urlpatterns.append(re_path('media/(?P<path>.*)', serve, {"document_root": MEDIA_ROOT}))
