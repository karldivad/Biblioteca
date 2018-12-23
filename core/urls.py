from django.urls import include, path

from . import views

urlpatterns = [
    path('', views.index),
    path('dashboard/', views.dashboard),
    path('', include('django.contrib.auth.urls')),
    path('', include('social_django.urls')),

    path('book/new', views.bookadd),
    path('book/delete/<int:id>', views.bookdelete),
    path('book/edit/<int:id>', views.bookedit),
]