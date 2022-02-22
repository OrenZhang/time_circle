from rest_framework.routers import SimpleRouter

from apps.circle.views import CategoryView

router = SimpleRouter()
router.register("category", CategoryView)

urlpatterns = router.urls
