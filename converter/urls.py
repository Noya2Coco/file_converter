from django.urls import path
from . import views

urlpatterns = [
    path('upload/', views.upload_file_view, name='upload_file'),
    path('convert/<uuid:conversion_token>/', views.convert_file_view, name='convert_file'),  # Utilise un token UUID
    path('download/<uuid:conversion_token>/', views.download_file_view, name='download_file'),  # Utilise un token UUID
]
