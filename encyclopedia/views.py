from django.shortcuts import render
from django.http import Http404
from django.shortcuts import redirect
import random
import markdown2
from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

# create views to show tech page and content
def entry(request, title):
    entry_content = util.get_entry(title)
    if entry_content is None:
        raise Http404("Entry not found")
    entry_content_html = markdown2.markdown(entry_content)
    return render(request, "encyclopedia/entry.html", {
        "title": title,
        "content": entry_content_html
    })

# implement wiki search
def search(request):
    query = request.GET.get('q')
    if util.get_entry(query):
        return redirect('entry', title=query)
    else:
        results = [entry for entry in util.list_entries() if query.lower() in entry.lower()]
        return render(request, "encyclopedia/search_results.html", {
            "query": query,
            "results": results
        })
    
    # view to create encyclopedia entry
def new_page(request):
    if request.method == "POST":
        title = request.POST.get("title")
        content = request.POST.get("content")
        if util.get_entry(title):
            return render(request, "encyclopedia/error.html", {
            "message": "Entry already exists."
        })
        else:
            util.save_entry(title, content)
            return redirect('entry', title=title)
    return render(request, "encyclopedia/new_page.html")

def random_page(request):
    entries = util.list_entries()
    random_entry = random.choice(entries)
    return redirect('entry', title=random_entry)