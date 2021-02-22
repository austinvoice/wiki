from django.urls import path

from . import views

# TODO replace random with dynamic field
# TODO replace wiki/ with capitalized URL
urlpatterns = [
    path("", views.index, name="index"),
    path("new", views.new, name="new"),
    path("wiki/{entry}", views.random, name="random"),
    path("<str:title>", views.entry, name="entry"),
    path("edit", views.edit, name="edit"),
    path("search", views.search, name="search")
]
