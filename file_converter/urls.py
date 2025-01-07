from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include

urlpatterns = [
    path('converter/', include('converter.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
