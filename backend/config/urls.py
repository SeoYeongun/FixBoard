from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/auth/', include('apps.users.urls')),
    path('api/posts/', include('apps.posts.urls')),
    path('api/comments/', include('apps.comments.urls')),
    path('api/votes/', include('apps.votes.urls')),
    path('api/tags/', include('apps.tags.urls')),
    path('api/answers/', include('apps.answers.urls')),
    path('api/notifications/', include('apps.notifications.urls')),
]