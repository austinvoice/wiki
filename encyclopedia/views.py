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
    content = forms.CharField(widget=forms.Textarea)

class ExistingWikiForm(forms.Form):
    title = forms.CharField(label="Title")
    content = forms.CharField(widget=forms.Textarea)

# index page, checks for new user or session
# TODO capitalize URL with Python function
def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

# create new entry by saving title, content into .md file
def new(request):
    if request.method == "POST":
        form = NewWikiForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            content = form.cleaned_data["content"]
            try:
                util.save_entry(title, content)
                return HttpResponse("<h1>Entry saved!<p><a href='/'>Home</a></h1>")
            except Exception:
                return HttpResponse("Sorry, error!")
    else:
        return render(request, "encyclopedia/new.html", {
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


# display the entry with dynamic URL by title
def entry(request, title):
    try:
        entry = util.get_entry(title)
        entry_html = markdown(entry)
        return render(request, "encyclopedia/entry.html", {
        "entry": entry_html
        })
    except Exception:
        return HttpResponse("Sorry, error!")


# edit existing entry and save new to disk
# TODO populate with existing content
def edit(request):
    try:
        form = ExistingWikiForm(initial={'title': 'Existing title', 'content': 'Existing content!'})
        return render(request, "encyclopedia/edit.html", {
            "form": form
        })
    except Exception:
        return render(request, "encyclopedia/index.html", {
            "form": ExistingWikiForm()
        })

# search function to find matching entry
# if file not found return file not found
def search(request):
    try:
        entry = util.get_entry(request.POST['q'])
        if entry != None:
            entry_html = markdown(entry)
            return render(request, "encyclopedia/entry.html", {
            "entry": entry_html
            })
        else:
            return HttpResponse("<h1>Sorry, file not found!<p><a href='/'>Home</a></h1>")
    except Exception:
        return HttpResponse("<h1>Sorry, error!<p><a href='/'>Home</a></h1>")
