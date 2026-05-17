from rest_framework.routers import DefaultRouter
from apps.posts.views import PostViewSet

router = DefaultRouter()

# '' → /api/posts/
# 자동으로 아래 URL 생성됨:
# GET    /api/posts/
# POST   /api/posts/
# GET    /api/posts/{id}/
# PATCH  /api/posts/{id}/
# DELETE /api/posts/{id}/
router.register('', PostViewSet, basename='post')

urlpatterns = router.urls