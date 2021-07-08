"""XXX_PROJECT_NAME_XXX URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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
from django.urls import path, include

from CollabTran.views import gitpull

urlpatterns = [
    path('', include('WebApp.urls')),
    path('admin/', admin.site.urls),
    path('gitpull', gitpull),

]

from django.contrib import admin

admin.site.site_header = 'CollabTran Administration'  # default: "Django Administration"
admin.site.index_title = 'CollabTran Administration'  # default: "Site administration"
admin.site.site_title = 'CollabTran Administration'  # default: "Django site admin"
