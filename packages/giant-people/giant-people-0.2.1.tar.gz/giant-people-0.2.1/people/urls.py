from django.urls import path

from .views import PeopleIndex

app_name = "events"

urlpatterns = [
    path("", PeopleIndex.as_view(), name="index"),
]
