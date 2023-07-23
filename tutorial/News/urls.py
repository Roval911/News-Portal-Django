from django.urls import path
from .views import PostList, NewsDetail, NewsSearch, NewsAdd, NewsEdit, NewsDelete, CategoryNewsDetail, subscribe, unsubscribe
urlpatterns = [
    path('', PostList.as_view()),
    path('<int:pk>', NewsDetail.as_view(), name='new_detail'),
    path('search', NewsSearch.as_view(), name='new_search'),
    path('add/', NewsAdd.as_view(), name='new_add'),
    path('<int:pk>/edit/', NewsEdit.as_view(), name='new_edit'),
    path('<int:pk>/delete/', NewsDelete.as_view(), name='new_delete'),
    path('cat/<int:pk>', CategoryNewsDetail.as_view(), name='cat'),
    path('subscribe/<int:pk>', subscribe, name='subscribe'),
    path('unsubscribe/<int:pk>', unsubscribe, name='unsubscribe'),
]