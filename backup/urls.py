from django.urls import path

from . import views


app_name = 'backup'

urlpatterns = [
    path('', views.index, name='index'),
    path('verify', views.verify, name='verify'),
    path('<int:job_id>/', views.detail, name='detail'),
]
