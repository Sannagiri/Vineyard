"""vineyard URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from django.urls import path,include
from django.conf.urls.static import static
from django.conf import settings
from User import views

urlpatterns = [
    # admin url for accessing the sqlite in server with global username and global password
    path('admin/', admin.site.urls),

    # for accessing all other urls to remain in the application
    path('',include('User.urls')),

    # for accessing the authorization urls like email and many other
    path('',include('django.contrib.auth.urls')),

    # functionality of Cart by involving the javascript
    path('updateitem/',views.updateItem,name='updateitem'),


    # adding the static root as we cannot give the static files separately
] + static(settings.STATIC_URL,document_root=settings.STATIC_ROOT)

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


