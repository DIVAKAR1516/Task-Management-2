from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TaskViewSet
from .auth_views import signup, login, logout, get_current_user

router = DefaultRouter()
router.register(r'tasks', TaskViewSet, basename='task')

urlpatterns = [
    path('auth/signup/', signup),
    path('auth/login/', login),
    path('auth/logout/', logout),
    path('auth/me/', get_current_user),
    path('', include(router.urls)),
]