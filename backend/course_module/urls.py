from rest_framework import routers
from .views import ModuleViewSet

# This is specific to DRF
# Generate the routing rules for category api to link to certain viewset
# r'' -> raw string
router = routers.DefaultRouter()
router.register(r'module', ModuleViewSet, 'module')

urlpatterns = router.urls
