from django.urls import path
from .views import UploadApi,ViewSatus
urlpatterns = [
   path('upload/',UploadApi.as_view(),name='upload'),
   path('status/',ViewSatus.as_view(),name='status')
]