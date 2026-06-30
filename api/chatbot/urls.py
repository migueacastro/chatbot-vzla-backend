from django.urls import path

from . import views

urlpatterns = [path("retrieve_info/", views.retrieve_info), name="retrieve_info"]
