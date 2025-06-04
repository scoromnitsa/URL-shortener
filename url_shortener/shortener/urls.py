from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ShortURLViewSet, redirect_view, StatsView

router = DefaultRouter()
router.register(r'urls', ShortURLViewSet, basename='shorturl')

urlpatterns = [
    path('', include(router.urls)),
    path('r/<str:short_code>/', redirect_view, name='redirect_view'),
    path('stats/', StatsView.as_view(), name='stats'),
]
