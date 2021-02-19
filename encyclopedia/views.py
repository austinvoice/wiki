# Django imports
from django.shortcuts import render
from . import util
from django.db import models
from django.http import HttpResponse, HttpResponseRedirect
from random import randint


# TODO capitalize URL with Python function
def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


# generate a random number in range of entries
# return entry
def random(request):
    entries = util.list_entries()
    selection = randint(0, len(entries) -1)
    entry = util.get_entry(entries[selection])
    return render(request, "encyclopedia/entry.html", {
        "entry": entry
    })


# TODO create def new to create an entry and save it
# TODO give access to existing content if already exists
# TODO use textarea and value from Markdown
def new(request):
    entry_content = models.TextField()
    return render(request, "encyclopedia/new.html", {
      "entry": entry_content
    })

# TODO get title from index
# TODO activate the edit button
def entry(request, title):
    return HttpResponse({util.get_entry(title)})


# TODO take title to select the correct entry
# TODO make the button save to disk
def edit(request):
    entries = util.list_entries()
    return render(request, "encyclopedia/edit.html", {
        "entry": util.get_entry(entries[0])
    })