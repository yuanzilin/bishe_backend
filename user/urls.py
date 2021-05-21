from django.urls import path
from user import views

urlpatterns = [
    path('login', views.login),
    path('register', views.register),
    path('logout', views.logout),
    path('getAllUser',views.getAllUser),
    path('deleteUser',views.deleteUser),
    path('reviewDeveloper', views.reviewDeveloper),
    path('LogOutUser',views.logoutuser),
]