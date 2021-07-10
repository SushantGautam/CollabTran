from django.conf.urls import url
from django.urls import include
from django.urls import path
from rest_framework import routers

from . import views
from .views import signup, LeaderBoard, Profile, logout_request, login_request

router = routers.DefaultRouter()

urlpatterns = (
    path("api/v1/", include(router.urls)),

)

urlpatterns += (
    path('', views.home, name='index'),
    path('navigateToPage', views.home, name='index'),
    path('LeaderBoard', LeaderBoard, name='LeaderBoard'),
)

urlpatterns += (
    path('signup', signup, name='signup'),
    path("logout", logout_request, name="logout"),
    url(r'^login/$', login_request, name='login'),

    path('Profile', Profile, name='Profile'),
)

urlpatterns += (
    path("contribution/", views.ContributionListView.as_view(), name="Contribution_list"),
    # path("Contribution/create/", views.ContributionCreateView.as_view(), name="Contribution_create"),
    path("contribution/detail/<int:pk>/", views.ContributionDetailView.as_view(),
         name="Contribution_detail"),
    # path("Contribution/update/<int:pk>/", views.ContributionUpdateView.as_view(),
    #      name="Contribution_update"),
)

# ajax
urlpatterns += (
    path('resolveURL', views.resolveURL, name='resolveURL'),
    path('SubmitContributions', views.SubmitContributions, name='SubmitContributions'),

)
