# Django imports
from django.shortcuts import render
from . import util
from django.db import models
from django.http import HttpResponse, HttpResponseRedirect
from random import randint
from markdown2 import markdown
from django import forms

# create a new form to accept entry data
class NewWikiForm(forms.Form):
    title = forms.CharField(label="Title")
    content = forms.CharField(label="Content")

class ExistingWikiForm(forms.Form):
    entry = forms.CharField(label="Title")

# index page, checks for new user or session
# TODO capitalize URL with Python function
def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def new(request):
    if request.method == "POST":
        form = NewWikiForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            content = forms.cleaned_data["content"]
            request.session[util.save_entry(title, content)]
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "new.html", {
                "form": form
            })
    else:
        return render(request, "new.html", {
            "form": NewWikiForm()
        })


# generate a random number in range of entries
def random(request):
    entries = util.list_entries()
    selection = randint(0, len(entries) - 1)
    entry = util.get_entry(entries[selection])
    entry_html = markdown(entry)
    return render(request, "encyclopedia/entry.html", {
        "entry": entry_html
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
    if request.method == "POST":
        form = ExistingWikiForm(request.POST)
        if form.is_valid():
            entry = form.cleaned_data["entry"]
            request.session["entry"] = [entry]
            return render(request, "encyclopedia/edit.html"), {
                "entry": entry,
                "form": form
            }
        else:
            return render(request, "encyclopedia/edit.html", {
            "entry": random(request),
            "form": form
             })
    else:
        return render(request, "edit.html", {
            "form": ExistingWikiForm()
        })

    return render(request, "encyclopedia/edit.html", {
        "form": form
    })

# search function to find matching entry
def search(request):
    # title = request.POST["q"]
    return render(request, "encyclopedia/entry.html", {
        "entry": markdown(util.get_entry("Django"))
    })