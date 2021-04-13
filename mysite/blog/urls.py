from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    # Post Views:
    # path('', views.post_list, name='post_list'),

    # Post List View:
    path('', views.PostListView.as_view(), name='post_list'),

    # Post Detail View:
    path('<int:year>/<int:month>/<int:day>/<slug:post>/',
         views.post_detail,
         name='post_detail'),

    # Post Share View:
    path('<int:post_id>/share/',
         views.post_share,
         name='post_share'),

]
