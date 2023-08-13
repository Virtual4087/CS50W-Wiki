from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<path:name>", views.search, name="addressbar"),
    path("search/", views.search_bar, name="searchbar"),
    path("search/<path:name>", views.search_results, name="search_results"),
    path("new/", views.new_entry, name="new"),
    path("edit/<path:name>", views.edit_page, name="edit"),
    path("random/", views.random, name="random")
]