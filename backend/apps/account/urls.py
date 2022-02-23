from rest_framework.routers import SimpleRouter

from apps.account.views import UserView

router = SimpleRouter()
router.register("", UserView)

urlpatterns = router.urls
