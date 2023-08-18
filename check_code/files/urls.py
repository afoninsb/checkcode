from django.urls import path

from . import views

app_name = 'files'

urlpatterns = [
    path('delete/<int:file_id>/', views.delete, name='delete'),
    path('reports/<int:file_id>/', views.reports, name='reports'),
    path('reupload/<int:file_id>/', views.reupload, name='reupload'),
    path('upload/', views.upload, name='upload'),
    path('', views.index, name='index'),
]
