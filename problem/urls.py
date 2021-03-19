from django.urls import path, include
from rest_framework.routers import DefaultRouter
from problem import views

router = DefaultRouter()
router.register('problem', views.ProblemViewSet)

urlpatterns = [
    path('', include(router.urls)),
]