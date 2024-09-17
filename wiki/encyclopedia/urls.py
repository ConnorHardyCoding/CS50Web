from django.urls import path

from . import views
import re

urlpatterns = [
    path("wiki/", views.index, name="index"),
    path("q", views.search, name="search"),
    path("create/", views.create, name="create"),
    path("random/", views.random, name="random"),
    path("edit/<str:title>", views.edit, name="edit"),
    path("wiki/<str:title>/", views.entry_page, name="entry")
]
