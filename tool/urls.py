from django.urls import path
from tool import views

urlpatterns = [
    path('upload_Tool', views.uploadTool),
    path('submit', views.saveTool),
    path('getdata', views.getData),
    path('deleteTool',views.deleteTool),
    path('updateTool',views.updateTool),
]