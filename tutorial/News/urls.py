from django.urls import path
from .views import PostList, NewsDetail
urlpatterns = [
    path('', PostList.as_view()),
    path('<int:pk>', NewsDetail.as_view())
]