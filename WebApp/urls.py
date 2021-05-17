from django.urls import path, include
from django.views.generic import TemplateView
from rest_framework import routers

from .views import signup, LeaderBoard, MyProfile, logout_request, login_request

router = routers.DefaultRouter()

urlpatterns = (
    path("api/v1/", include(router.urls)),

)

urlpatterns += (
    path('', TemplateView.as_view(template_name='home.html'), name='index'),
    path('LeaderBoard', LeaderBoard, name='LeaderBoard'),
)

urlpatterns += (
    path('signup', signup, name='signup'),
    path("logout", logout_request, name="logout"),
    path("login", login_request, name="login"),

    path('MyProfile', MyProfile, name='MyProfile'),
)
