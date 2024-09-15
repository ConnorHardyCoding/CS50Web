from django.urls import path

from . import views
import re

urlpatterns = [
    path("", views.index, name="index"),
    path("q", views.search, name="search"),
    path("create/", views.create, name="create"),
    path("random", views.random, name="random"),
    path("edit/", views.edit, name="edit"),
    path("<str:title>/", views.entry_page, name="entry")
]
