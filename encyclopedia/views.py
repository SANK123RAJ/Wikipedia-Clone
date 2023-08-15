from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
import markdown
from django.urls import reverse,path
from . import util,urls,views
from django.urls import resolve
import os
import random



def newpage(request):
    if request.method == "POST":
        title = request.POST.get("title")
        markdown = request.POST.get("markdown")
        isedit = request.POST.get("edit")
        if title in util.list_entries() and isedit != "edit":
            return render(request,"encyclopedia/pageexists.html",{
    "random": random.choice(util.list_entries())
})
        else:
            util.save_entry(title,markdown)
            urls.listofpaths.append(path("wiki/"+title, views.title, name = (title)))
            return HttpResponseRedirect(reverse(title),{
    "random": random.choice(util.list_entries())
})
    else:    
        return render(request,"encyclopedia/newpage.html",{
    "random": random.choice(util.list_entries())
})

    



def index(request):
    if request.method == 'POST':
        name = request.POST.get('q')
        if name in util.list_entries():
           return HttpResponseRedirect(reverse(name),{
    "random":  random.choice(util.list_entries())
}
)
        else:
            similar_entries = []
            for entries in util.list_entries():
                if name in entries:
                    similar_entries.append(entries)
            if len(similar_entries) == 0:
                return render(request,"encyclopedia/error.html",{
    "random":  random.choice(util.list_entries())
}
)
            else:
                return render(request,"encyclopedia/Similarpages.html",{
                "entries" : similar_entries,
                "name": name,
                "random":  random.choice(util.list_entries())})
    else:
        return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries(),
        "random":  random.choice(util.list_entries())
    })



def error(request,title):
    return render(request,"encyclopedia/error.html",{
    "random": random.choice(util.list_entries())
})




def title(request):
    title = resolve(request.path_info).url_name
    file = util.get_entry(title)
    if file != None:
        filename = "entries/"+title+".md"
        
        with open(filename, 'r') as markdown_file:
           markdown_text = markdown_file.read()


        html = markdown.markdown(markdown_text)
        with open('htmlconversion.html', 'r') as file:
           html_content = file.read()
           newfile = html_content.replace('<!-- INSERT HERE -->', html)

           save_path = r'encyclopedia\templates\encyclopedia'
           name_of_file = "updated"
           completeName = os.path.join(save_path, name_of_file+".html")        
           file1 = open(completeName, "w")
           file1.write(newfile)
           file1.close()
        file.close()
        return render(request,"encyclopedia/updated.html",{
            "title": title,
            "random": random.choice(util.list_entries())

        }) 
    else:
       return render(request,"encyclopedia/error.html",{
           "random": random.choice(util.list_entries())
       })



def edit(request):
    if request.method == "POST":
       title = request.POST.get('test')
       file = util.get_entry(title)
       filename = "entries/"+title+".md"
       with open(filename, 'r') as markdown_file:
           markdown_text = markdown_file.read()
       return render(request,"encyclopedia/edit.html",{
           "markdown": markdown_text,
           "title": title,
           "random": random.choice(util.list_entries())
       })

