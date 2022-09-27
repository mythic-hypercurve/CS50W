from http.client import HTTPResponse
from django.shortcuts import render
import markdown

from . import util

def markdownToHtml(entry):
    content = util.get_entry(entry)
    markdowner = markdown.Markdown()
    if content == None:
        return None
    else:    
        return markdowner.convert(entry)

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def page(request, entry):
    contentHtml = markdownToHtml(entry)
    if contentHtml == None:
        return render(request, "encyclopedia/error.html")
    else:
        return render(request, "encyclopedia/entry.html")  