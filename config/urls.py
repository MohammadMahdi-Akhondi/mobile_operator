from django.urls import path, include
from django.contrib import admin


urlpatterns = [
    # Admin URLs
    path('admin/', admin.site.urls),

    # Core SOAP endpoints
    path('api/', include('core.urls')),
]
