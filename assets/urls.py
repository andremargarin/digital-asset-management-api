from assets import views
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register(r'asset-file', views.AssetFileViewSet, basename='assets')
urlpatterns = router.urls
