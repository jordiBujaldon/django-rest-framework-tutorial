from blog.models import Post
from blog.serializers import PostSerializer

from rest_framework import generics
from rest_framework.permissions import BasePermission, IsAuthenticatedOrReadOnly, SAFE_METHODS


class PostUserWritePermission(BasePermission):
    message = 'Editing posts is restricted to the author only'

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        return obj.author == request.user


class PostList(generics.ListCreateAPIView):
    queryset = Post.post_objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class PostDetail(generics.RetrieveUpdateDestroyAPIView, PostUserWritePermission):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [PostUserWritePermission]

    def test(self):
        pass
