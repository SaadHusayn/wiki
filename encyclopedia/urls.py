from django.urls import path

from . import views
app_name = 'encyclopedia'

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/new", views.createNewPage, name="createNewPage"),
    path("wiki/random", views.randomPage, name="randomPage"),
    path("wiki/edit/<str:pageTitle>", views.editPage, name="editPage"),
    path("wiki/<str:pageTitle>", views.viewPage, name="viewPage")    
]
