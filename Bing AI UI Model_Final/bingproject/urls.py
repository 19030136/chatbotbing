from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('', include('bingapp.urls')),  # Include your app's URL patterns
    path('admin/', admin.site.urls),  # URL pattern for the admin site
]
