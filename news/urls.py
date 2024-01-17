from django.urls import path
from .views import PostsList, PostDetail, PostCreate, PostUpdate, PostDelete, ArticleUpdate, ArticleDelete


urlpatterns = [
   path('', PostsList.as_view(), name='post_list'),
   path('<int:pk>', PostDetail.as_view(), name='post_detail'),
   path('create/', PostCreate.as_view(), name='news.urls'),
   path('<int:pk>/edit/', PostUpdate.as_view(), name='news_edit'),
   path('<int:pk>/delete/', PostDelete.as_view(), name='news_delete'),
   path('articles/create/', PostCreate.as_view(), name='article_create'),
   path('articles/<int:pk>/edit/', ArticleUpdate.as_view, name='article_edit'),
   path('articles/<int:pk>/delete/', ArticleDelete.as_view, name='article_delete'),
]