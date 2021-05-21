from django.urls import path
from service import views
urlpatterns = [
    path('submit', views.submitService),
    path('upload_service',views.saveServiceFile),
    path('getdata',views.getData),
    path('deleteService',views.deleteService),
    path('getServiceIntro',views.getServiceIntro),
]