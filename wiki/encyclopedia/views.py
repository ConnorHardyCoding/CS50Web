from django.shortcuts import render
from django import forms
from . import util
import re
from random import choice

class QueryForm(forms.Form):
    query = forms.CharField()

class EntryForm(forms.Form):
    title = forms.CharField()
    entry = forms.CharField(widget=forms.Textarea(attrs={
        'style': 'width: 80%; height: 50vh;'
    }))

def index(request):

    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries(),
    })

def entry_page(request, title=""):

    return render(request, "encyclopedia/encyclopedia.html", {
        "entry": util.get_entry(title),
        "title": title
    })

def create(request):
    form = EntryForm(request.GET)
    if request.method == "POST":
        form = EntryForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            entry = form.cleaned_data["entry"]
            if title not in util.list_entries():
                util.save_entry(title, entry)
                return render(request, "encyclopedia/encyclopedia.html", {
                "entry": util.get_entry(title),
                "title": title
            })

            else:
                return render(request, "encyclopedia/create.html", {
                    "forms": form,
                    "error": True
                })

    return render(request, "encyclopedia/create.html", {
        "forms": form
    })

def search(request):
    form = QueryForm(request.GET)
    if form.is_valid():
        query = form.cleaned_data["query"]
        if util.get_entry(query) == None:
            search_list = [x for x in util.list_entries() if query.lower() in x.lower()]
            return render(request, "encyclopedia/search.html", {
                "entries": search_list,
                "query": query
            })
        else:
            return render(request, "encyclopedia/encyclopedia.html", {
                "entry": util.get_entry(query),
                "title": query
            })

def random(request):
    title = choice(util.list_entries())
    return render(request, "encyclopedia/encyclopedia.html", {
        "entry": util.get_entry(title),
        "title": title
    })

def edit(request):
    pass