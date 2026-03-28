from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TaskViewSet
from .auth_views import signup, login

router = DefaultRouter()
router.register(r'tasks', TaskViewSet)

urlpatterns = [
path('signup/', signup),
    path('login/', login),
    path('', include(router.urls)),
]