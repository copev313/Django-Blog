from django.urls import path
from . import views
from .feeds import LatestPostsFeed


app_name = 'blog'

urlpatterns = [
    # Post List View:
    path('', views.post_list, name='post_list'),

    # Class-based Post List View:
    #path('', views.PostListView.as_view(), name='post_list'),

    # Post Detail View:
    path('<int:year>/<int:month>/<int:day>/<slug:post>/',
         views.post_detail,
         name='post_detail'),

    # Post Share View:
    path('<int:post_id>/share/',
         views.post_share,
         name='post_share'),

     # Posts by Tag View:
     path('tag/<slug:tag_slug>/',
          views.post_list,
          name='post_list_by_tag'),
     
     # Latest Posts Feed View:
     path('feed/', LatestPostsFeed(), name='post_feed'),

]
