from http.client import HTTPResponse
from django.shortcuts import render
from markdown2 import Markdown
import random

from . import util
# from Wiki import encyclopedia
def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def convertMarkdownToHtml(title):
     entryMarkdown = util.get_entry(title)
     if entryMarkdown is None:
        return None
     entryHtml= Markdown().convert(entryMarkdown)
     return entryHtml

def entry(request, title):
    
    entryMarkdown = util.get_entry(title)
    if entryMarkdown is not None:
        entryHtml= convertMarkdownToHtml(title)
        return render(request, "encyclopedia/entry.html", {
            "title": title,
            "content": entryHtml 
        })  
    else:
        return render(request, "encyclopedia/error.html", {
            "message": "The entry you are looking for does not exist"
        })
        
def search(request):
    if request.method == "POST":
        entrySearch = request.POST['q']
        htmlContent = convertMarkdownToHtml(entrySearch)
        if htmlContent is not None:
            return render(request, "encyclopedia/entry.html", {
            "title": entrySearch,
            "content": htmlContent 
        })      
        else: 
            allEntries = util.list_entries()
            recommendedEntries= []
            for entry in allEntries:
                if entrySearch.lower() in entry.lower():
                    recommendedEntries.append(entry)
            return render(request, "encyclopedia/search.html",{
                "recommendations" : recommendedEntries
            })               
def newPage(request):
    if request.method == "GET":
        return render(request, "encyclopedia/new.html")
    else:
        title = request.POST['title']
        content = request.POST['content']
        titleExists = util.get_entry(title)
        if titleExists is not None:
            return render (request,"encyclopedia/error.html", { 
                "message":"The Entry page you are trying to create already exists."
            })
        else:
            util.save_entry(title, content)
            htmlContent = convertMarkdownToHtml(title)
            return render(request, "encyclopedia/entry.html", {
                "title": title,
                "content": htmlContent,
            })

def edit(request):
    if request.method == 'POST':
        title = request.POST['entryTitle']
        content = util.get_entry(title)
        return render(request, "encyclopedia/edit.html", {
            "title": title,
            "content": content
        })

def saveEdit(request):
    if request.method =="POST":
        title = request.POST['title']
        content = request.POST['content']
        util.save_entry(title, content)
        htmlContent = convertMarkdownToHtml(title)
        return render(request, "encyclopedia/entry.html",{
            "title": title,
            "content":htmlContent                
        })       

def rand(request):
    allEntries= util.list_entries()
    rand_entry = random.choice(allEntries)
    htmlContent= convertMarkdownToHtml(rand_entry)
    return render(request, "encyclopedia/entry.html", {
        "title": rand_entry,
        "content":htmlContent
    })