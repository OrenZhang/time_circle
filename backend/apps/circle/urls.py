from rest_framework.routers import SimpleRouter

from apps.circle.views import CategoryView, ItemView

router = SimpleRouter()
router.register("category", CategoryView)
router.register("item", ItemView)

urlpatterns = router.urls
