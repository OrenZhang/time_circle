from rest_framework.routers import SimpleRouter

from apps.circle.views import CategoryView, ItemView, OverviewView, StatisticView

router = SimpleRouter()
router.register("category", CategoryView)
router.register("item", ItemView)
router.register("overview", OverviewView)
router.register("statistic", StatisticView)

urlpatterns = router.urls
