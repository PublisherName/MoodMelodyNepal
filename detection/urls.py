from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from detection import views

urlpatterns = [
    path("", views.index, name="index"),
    path("expression", views.expression, name="expression"),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
