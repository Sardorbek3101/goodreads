from django.urls import path
from rest_framework.routers import DefaultRouter
from api.views import BookReviewsViewSet
# from api.views import BookReviewDetailAPIView, BookReviewListAPIView

router = DefaultRouter()
router.register('reviews', BookReviewsViewSet, basename="reviews")

app_name = "api"
urlpatterns = router.urls
