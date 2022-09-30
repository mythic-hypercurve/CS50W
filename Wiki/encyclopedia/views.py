from http.client import HTTPResponse
from django.shortcuts import render
from markdown2 import Markdown

from . import util

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, title):
    entryMarkdown = util.get_entry(title)
    if entryMarkdown != None:
        entryHtml= Markdown().convert(entryMarkdown)
        return render(request, "encyclopedia/entry.html", {
            "title": title,
            "entry": entryHtml 
        })  
    else:
        return render(request, "encyclopedia/error.html", {
            "message": "The entry you are looking for does not exist"
        })
        