from django.contrib.auth.decorators import login_required
from django.urls import include
from django.urls import path
from django.views.generic import TemplateView
from rest_framework import routers

from . import views
from .views import signup, LeaderBoard, MyProfile, logout_request, login_request

from django.contrib import admin

admin.site.site_header = 'CollabTran Administration'                    # default: "Django Administration"
admin.site.index_title = 'CollabTran Administration'                 # default: "Site administration"
admin.site.site_title = 'CollabTran Administration' # default: "Django site admin"


router = routers.DefaultRouter()

urlpatterns = (
    path("api/v1/", include(router.urls)),

)

urlpatterns += (
    path('', TemplateView.as_view(template_name='home.html'), name='index'),
    path('translate', login_required(TemplateView.as_view(template_name='translate.html')), name='translate'),
    path('LeaderBoard', LeaderBoard, name='LeaderBoard'),
)

urlpatterns += (
    path('signup', signup, name='signup'),
    path("logout", logout_request, name="logout"),
    path("login", login_request, name="login"),

    path('MyProfile', MyProfile, name='MyProfile'),
)

urlpatterns += (
    path("Contribution/", views.ContributionListView.as_view(), name="WebApp_Contribution_list"),
    path("Contribution/create/", views.ContributionCreateView.as_view(), name="WebApp_Contribution_create"),
    path("Contribution/detail/<int:pk>/", views.ContributionDetailView.as_view(),
         name="WebApp_Contribution_detail"),
    path("Contribution/update/<int:pk>/", views.ContributionUpdateView.as_view(),
         name="WebApp_Contribution_update"),
)


#ajax
urlpatterns += (
    path('resolveURL', views.resolveURL, name='resolveURL'),

)


