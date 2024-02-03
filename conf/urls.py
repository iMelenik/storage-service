from django.contrib import admin
from django.urls import path, include

app_name = "conf"

urlpatterns = [
    path("", include('upload.urls')),
    path('admin/', admin.site.urls),
]
