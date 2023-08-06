from django.urls import path
from . import views

urlpatterns = [
    path("", views.MainView.as_view(), name = 'home'),
    path("barber", views.MainView.as_view(), name = 'barber'),
    path("about", views.MainView.as_view(), name = 'about'),
    path("contacts", views.MainView.as_view(), name = 'contacts'),
    path("blog", views.MainView.as_view(), name = 'blog'),
    ]
