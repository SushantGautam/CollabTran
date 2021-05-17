from django.urls import path, include
from django.views.generic import TemplateView
from rest_framework import routers

from . import api
from . import views

router = routers.DefaultRouter()

urlpatterns = (
    path("api/v1/", include(router.urls)),

)

urlpatterns += (
    path('', TemplateView.as_view(template_name='index.html'), name='index'),
)
