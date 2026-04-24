from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    CommonToolCategoryViewSet,
    CommonToolTagViewSet,
    CommonToolResourceViewSet,
    CommonToolAccessLogViewSet,
)

router = DefaultRouter()
router.register(r'categories', CommonToolCategoryViewSet)
router.register(r'tags', CommonToolTagViewSet)
router.register(r'resources', CommonToolResourceViewSet)
router.register(r'access-logs', CommonToolAccessLogViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
