from car_maintenance import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'cars', views.CarViewSet, basename='cars')

urlpatterns = router.urls