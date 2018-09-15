from django.urls import path

from . import views

app_name = 'imagegen'
urlpatterns = [
    path("simple/<int:width>x<int:height>", views.simple, name='simple'),
    path("mandelbrot/<int:width>x<int:height>", views.mandelbrot, name='mandelbrot'),
    path("saved/<slug:slug>", views.saved_image, name='saved')
]
