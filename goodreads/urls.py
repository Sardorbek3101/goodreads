from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from .views import home_page
from posts.views import PostsView


urlpatterns = [
    path('', PostsView.as_view(), name="landing_page"),
    path('home/', home_page, name="home_page"),
    path('admin/', admin.site.urls),
    path('users/', include('users.urls')),
    path('books/', include("books.urls")),
    path('friends/', include("friends.urls")),
    path('posts/', include("posts.urls")),
    path("api/", include("api.urls")),
    path('api-auth/', include('rest_framework.urls')),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
