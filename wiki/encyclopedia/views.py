from django.shortcuts import render, redirect
from django import forms
from . import util
from random import choice
import markdown2 as md

class QueryForm(forms.Form):
    query = forms.CharField()

class EntryForm(forms.Form):
    title = forms.CharField()
    entry = forms.CharField(widget=forms.Textarea(attrs={'style': 'width: 80%; height: 50vh;'}), initial="")

class EditForm(forms.Form):
    entry = forms.CharField(widget=forms.Textarea(attrs={'style': 'width: 80%; height: 50vh;'}), initial="")

def index(request):

    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries(),
    })

def entry_page(request, title=""):
    for item in util.list_entries():
            if title.lower() == item.lower():
                title = item
    if title in util.list_entries():
        entry = md.markdown(util.get_entry(title))
    else:
        entry = None
    return render(request, "encyclopedia/encyclopedia.html", {
        "entry": entry,
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
                return redirect('entry', title)

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
        for item in util.list_entries():
            if query.lower() == item.lower():
                query = item
        if util.get_entry(query) == None:
            search_list = [x for x in util.list_entries() if query.lower() in x.lower()]
            return render(request, "encyclopedia/search.html", {
                "entries": search_list,
                "query": query
            })
        else:
            return redirect('entry', query)

def random(request):
    title = choice(util.list_entries())
    return redirect('entry', title)

def edit(request, title):
    if request.method == "POST":
        form = EditForm(request.POST)
        if form.is_valid():
            entry = form.cleaned_data["entry"]
            util.save_entry(title, entry)
            return redirect('entry', title)
    initial_data = {
        "title": title,
        "entry": util.get_entry(title)
    }
    form = EntryForm(initial=initial_data)
    return render(request, "encyclopedia/edit.html", {
        "forms": form,
        "title": title
    })

    