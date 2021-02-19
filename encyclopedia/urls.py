from django.urls import path

from . import views

# TODO replace random with dynamic field
# TODO replace wiki/ with capitalized URL
urlpatterns = [
    path("", views.index, name="index"),
    path("new/", views.new, name="new"),
    path("random/", views.random, name="random"),
    path("wiki/{entry}", views.entry, name="entry"),
    path("edit", views.edit, name="edit")
]
