from django.urls import path

from . import views,util

entries = util.list_entries()


listofpaths = []
for entry in entries:
    listofpaths.append(path("wiki/"+entry, views.title, name = (entry)))
listofpaths.append(path("wiki/"+"", views.index, name="index"))
listofpaths.append(path("wiki/"+"<str:title>",views.error,name = "error"))
listofpaths.append(path("wiki/"+"encyclopedia/newpage", views.newpage, name="newpage"))
listofpaths.append(path("wiki/"+"encyclopedia/edit", views.edit, name="edit"))
urlpatterns = listofpaths

