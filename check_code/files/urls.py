from django.urls import path

from . import views

app_name = 'files'

urlpatterns = [
    path('upload/', views.upload, name='upload'),
    path('report/<int:file_id>/', views.report, name='report'),
    path('', views.index, name='index'),
]
