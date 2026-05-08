from rest_framework.routers import DefaultRouter
from apps.votes.views import VoteViewSet

router = DefaultRouter()
router.register('', VoteViewSet, basename='vote')

urlpatterns = router.urls