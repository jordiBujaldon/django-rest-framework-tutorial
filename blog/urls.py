from blog.views import PostDetail, PostList

from django.urls import path


app_name = 'blog'

urlpatterns = [
    path('', PostList.as_view(), name='post_list'),
    path('<int:pk>/',  PostDetail.as_view(), name='post_details')
]
