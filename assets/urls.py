from django.urls import path
from assets import views


urlpatterns = [
    path('upload/', views.FileUploadView.as_view(), name='asset_create'),
    path('list/', views.FileListView.as_view(), name='asset_list'),
    path('delete/<int:pk>/', views.FileDestroyView.as_view(), name='asset_delete'),
    path('detail/<int:pk>/', views.FileRetrieveView.as_view(), name='asset_detail'),
]
