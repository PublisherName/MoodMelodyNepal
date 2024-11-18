from django.urls import path

from detection import views

urlpatterns = [
    path("", views.index, name="index"),
    path("expression", views.expression, name="expression"),
]
