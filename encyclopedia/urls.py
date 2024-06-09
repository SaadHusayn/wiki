from django.urls import path

from . import views
app_name = 'encyclopedia'

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/create-new-page", views.createNewPage, name="createNewPage"),
    path("wiki/edit-page/<str:title>", views.editPage, name="editPage"),
    path("wiki/<str:title>", views.viewPage, name="viewPage")    
]
