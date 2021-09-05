from car_maintenance import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'car', views.CarViewSet, basename='cars')

urlpatterns = router.urls