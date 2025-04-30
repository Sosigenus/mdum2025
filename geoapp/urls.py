from django.urls import path
from . import views

urlpatterns = [
    path('upload/', views.upload_json, name='upload_json'),
    path('records/', views.records_table, name='records_table'),
    path('map/', views.leaflet_map, name='leaflet_map'),
]
