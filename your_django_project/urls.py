# your_django_project/urls.py

from django.contrib import admin
# Make sure 'include' is imported here
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    # This is the crucial line that connects your app.
    # It tells Django: "For any URL that isn't '/admin/', go look for instructions in 'medical_assistant_app.urls'".
    path('', include('medical_assistant_app.urls')),
]