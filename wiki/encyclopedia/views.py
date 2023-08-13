from django.shortcuts import render, redirect
import markdown2
from . import util
from django.http import HttpResponse
from django import forms
import re


class new_entry_form(forms.Form):
    title_area = forms.CharField(label= "Title",
        min_length= 1,
        max_length= 30,
        widget= forms.TextInput(attrs= {"placeholder" : "Title of your page", "autocomplete" : "off"}))
    
    markdown_area = forms.CharField(label= "Markdown Content", 
        min_length= 1,
        widget= forms.Textarea(attrs= {"placeholder" : "Content of your page in markdown"}))


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def search(request, name):
    if not name:
        return redirect("index")
    for entry in util.list_entries():
        if name == entry:
            markdown = markdown2.markdown(util.get_entry(name))
            return render(request, "encyclopedia/search.html", {
                "title" : name,
                "content" : markdown
            })
        
        elif name.lower() == entry.lower():
            return redirect('addressbar', name= entry)
        
    return render(request, "encyclopedia/Error.html", {
        "title" : name
    })


def search_bar(request):
    if request.method != "POST":
        return redirect('index')
    
    search = request.POST.get('q') 
    
    for entry in util.list_entries():

        if search.lower() == entry.lower():
            return redirect('addressbar', name= entry) 
        
    return redirect('search_results', name=search)


def search_results(request, name):
    result = []
    for entry in util.list_entries():
        if name.lower() == entry.lower():
            return redirect('addressbar', name= entry)
        
        elif name.lower() in entry.lower():
            result.append(entry)
    
    return render(request, "encyclopedia/results.html", {
        "title" : name,
        "result" : result
    })


def new_entry(request):
    if request.method != "POST":
        return render(request, "encyclopedia/new_entry.html", {
            "add_form" : new_entry_form()
        })
    
    form = new_entry_form(request.POST)
    if form.is_valid():
        title = form.cleaned_data['title_area']
        markdown = form.cleaned_data['markdown_area']
        
        for entry in util.list_entries():
            if title.lower() == entry.lower():
                return render(request, "encyclopedia/new_entry.html", {
                    "add_form" : form,
                    "error" : "already_exists"
                })
            
        title = title.capitalize()
        util.save_entry(title, markdown)              
        return redirect('addressbar', name= title)
            
    return render(request, "encyclopedia/new_entry.html", {
                    "add_form" : form,
                })


def edit_page(request, name):
    if request.method == "POST":
        form = new_entry_form(request.POST)
        if form.is_valid():
            markdown = form.cleaned_data['markdown_area']
            util.save_entry(name, markdown)
        else:
            return render(request, "encyclopedia/edit.html", {
                "add_form" : form
            })
            
        return redirect("addressbar", name= name)
      
    for entry in util.list_entries():
        if entry == name:
           
            form = new_entry_form(initial={
                'title_area': entry, 
                'markdown_area' :  util.get_entry(entry).replace('\r\n', '\n')
            })
            form.fields['title_area'].widget.attrs['readonly'] = True
            return render(request, "encyclopedia/edit.html", {
                'add_form' : form          
            })
        elif entry.lower() == name.lower():
            return redirect("edit", name= entry)
    return redirect("addressbar", name= name)
    

def random(request):
    import random
    random_page = random.choice(util.list_entries())
    return redirect('addressbar', name= random_page)
