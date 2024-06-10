from django.shortcuts import render
from django.core.files.storage import default_storage
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from . import util
from .forms import NewEditForm, NewPageForm, NewSearchEntryForm
import markdown2
    

def index(request):
    if util.isMethodPost(request):
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

def viewPage(request, pageTitle):
    markdownContent = util.get_entry(pageTitle)
    if markdownContent == None:
        return render(request, 'encyclopedia/errorPage.html', {
            "pageTitle" : pageTitle,
            "errorMessage": f"/wiki/{pageTitle} Page Not Found",
            "searchEntryForm": NewSearchEntryForm()
        })
    else:
        html = markdown2.markdown(markdownContent)
        return render(request, 'encyclopedia/viewPage.html', {
            "html" : html, 
            "pageTitle" : pageTitle,
            "searchEntryForm": NewSearchEntryForm()
        })
    
def createNewPage(request):
    if(util.isMethodPost(request)):
        newPageData = NewPageForm(request.POST)
        if newPageData.is_valid():
            pageTitle = newPageData.cleaned_data["pageTitle"]
            markdownContent = newPageData.cleaned_data["markdownContent"]
            if(util.isValidPageTitle(pageTitle)):
                newPageFile = default_storage.open(f"entries/{pageTitle}.md", mode="w")
                newPageFile.write(markdownContent)
            else:
                errorMessage = f"Page with title {pageTitle.lower()} already exists"
                return render(request, 'encyclopedia/errorPage.html', {
                    "pageTitle" : pageTitle,
                    "errorMessage": errorMessage,
                    "searchEntryForm": NewSearchEntryForm()
                })
                
    
    return render(request, 'encyclopedia/createNewPage.html',{
        "newPageForm":NewPageForm(),
        "searchEntryForm": NewSearchEntryForm(),
        "searchEntryForm": NewSearchEntryForm()
    })

def editPage(request, pageTitle):
    if(util.isMethodPost(request)):
        editFormData = NewEditForm(request.POST)
        if(editFormData.is_valid()):
            markdownContent = editFormData.cleaned_data["markdownContent"]
            editPageFile = default_storage.open(f"entries/{pageTitle}.md", mode="w")
            editPageFile.write(markdownContent)
            return HttpResponseRedirect(reverse("encyclopedia:viewPage", args=(pageTitle, )))

    return render(request, "encyclopedia/editPage.html", {
        "pageTitle":pageTitle,
        "editPageForm": NewEditForm(initial={"markdownContent":util.get_entry(pageTitle)}),
        "searchEntryForm": NewSearchEntryForm()
    })

def randomPage(request):
    pageTitle = util.getRandomPageTitle()
    return HttpResponseRedirect(reverse("encyclopedia:viewPage", args=(pageTitle, )))