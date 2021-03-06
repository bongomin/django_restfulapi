from django.urls import include, path
from rest_framework import routers
from .views import UserViewSet, GroupViewSet, PostsViewSet, TagViewSet

router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'groups', GroupViewSet)
router.register(r'posts', PostsViewSet)
router.register(r'Tags', TagViewSet)

# Additionally, I include login URLs for the browsable API.
urlpatterns = [
    # thsi helps to fetch the endpoints of the routers
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]
