from django.shortcuts import render
from django.core.files.storage import default_storage
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from . import util
from django import forms
import markdown2

def isMethodPost(request):
    return (request.method == "POST")

class NewSearchEntryForm(forms.Form):
    searchEntry = forms.CharField(label="",widget=forms.TextInput(attrs={'placeholder': 'Search Encyclopedia'}))

class NewPageForm(forms.Form):
    pageTitle = forms.CharField(label="Title", widget=forms.TextInput(attrs={"class":"form-group"}))
    markdownContent = forms.CharField(label="MarkDown Content", widget=forms.Textarea(attrs={"class":"form-group"}))

class NewEditForm(forms.Form):
    def __init__(self, title=""):
        self.markdownContent = forms.CharField(label="MarkDown Content", widget=forms.Textarea(attrs={"class":"form-group", "value": util.get_entry(title)}))

    


    

def index(request):
    if isMethodPost(request):
        searchEntryForm = NewSearchEntryForm(request.POST)
        if searchEntryForm.is_valid():
            searchEntry = searchEntryForm.cleaned_data["searchEntry"]
            entries = util.list_entries()
            entriesMatchingSearch = []
            for entry in entries:
                if searchEntry.lower() == entry.lower():
                    return HttpResponseRedirect(reverse("encyclopedia:viewPage", args=(entry,)))
                elif searchEntry.lower() in entry.lower():
                    entriesMatchingSearch.append(entry)

        return render(request, 'encyclopedia/index.html', {
            "entries": entriesMatchingSearch,
            "heading": "Search Results",
            "searchEntryForm": searchEntryForm
        })

    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries(),
        "heading": "All Pages",
        "searchEntryForm": NewSearchEntryForm()
    })

def viewPage(request, title):
    markdownContent = util.get_entry(title)
    if markdownContent == None:
        return render(request, 'encyclopedia/errorPage.html', {
            "title" : title,
            "errorMessage": f"/wiki/{title} Page Not Found",
            "searchEntryForm": NewSearchEntryForm()
        })
    else:
        html = markdown2.markdown(markdownContent)
        return render(request, 'encyclopedia/viewPage.html', {
            "html" : html, 
            "title" : title,
            "searchEntryForm": NewSearchEntryForm()
        })
    
def createNewPage(request):
    if(isMethodPost(request)):
        newPageData = NewPageForm(request.POST)
        if newPageData.is_valid():
            pageTitle = newPageData.cleaned_data["pageTitle"]
            markdownContent = newPageData.cleaned_data["markdownContent"]
            if(pageTitle in util.list_entries()):
                return render(request, 'encyclopedia/errorPage.html', {
                    "title" : pageTitle,
                    "errorMessage": f"Page with title {pageTitle} already exists",
                    "searchEntryForm": NewSearchEntryForm()
                })
            else:
                newPageFile = default_storage.open(f"entries/{pageTitle}.md", mode="w")
                newPageFile.write(markdownContent)
                
    
    return render(request, 'encyclopedia/createNewPage.html',{
        "newPageForm":NewPageForm(),
        "searchEntryForm": NewSearchEntryForm(),
        "searchEntryForm": NewSearchEntryForm()
    })

def editPage(request, title):
    return render(request, "encyclopedia/editPage.html", {
        "title":title,
        "editPageForm": NewEditForm(title),
        "searchEntryForm": NewSearchEntryForm()
    })