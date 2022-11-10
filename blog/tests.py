from blog.models import Category, Post

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient, APITestCase


class TestPostModel(TestCase):
    @classmethod
    def setUpTestData(cls):
        Category.objects.create(name='django')
        User.objects.create_user(username='user', password='1234')
        Post.objects.create(title='Post title', excerpt='Post excerpt', content='Post content', slug='post-title',
                            status='published', category_id=1, author_id=1)

    def test_blog_content(self):
        post = Post.post_objects.get(id=1)
        category = Category.objects.get(id=1)
        # Asserts
        self.assertEqual(f'{post.author}', 'user')
        self.assertEqual(f'{post.title}', 'Post title')
        self.assertEqual(f'{post.content}', 'Post content')
        self.assertEqual(f'{post.status}', 'published')
        self.assertEqual(str(post), post.title)
        self.assertEqual(str(category), category.name)


class TestPostAPI(APITestCase):
    @classmethod
    def setUpTestData(cls):
        Category.objects.create(name='django')
        User.objects.create_user(username='user', password='1234')
        User.objects.create_user(username='user2', password='1234')
        Post.objects.create(title='Post title', excerpt='Post excerpt', content='Post content', slug='post-title',
                            status='published', category_id=1, author_id=1)

    def test_get_post_list(self):
        url = reverse('blog:post_list')
        response = self.client.get(url, format='json')
        # Assert status
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_post_post(self):
        data = {
            'title': 'Post title',
            'excerpt': 'Post excerpt',
            'content': 'Post content',
            'author': 1
        }
        url = reverse('blog:post_list')
        self.client.login(username='user', password='1234')
        response = self.client.post(url, data, format='json')
        # Assert
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get_post_detail(self):
        # Login user
        self.client.login(username='user', password='1234')
        # Post data
        data = {
            'title': 'Post title',
            'excerpt': 'Post excerpt',
            'content': 'Post content',
            'author': 1
        }
        url_post = reverse('blog:post_list')
        self.client.post(url_post, data, format='json')
        # Get data detail
        url_get = reverse('blog:post_details', kwargs={'pk': 2})
        response = self.client.get(url_get, format='json')
        # Assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_put_post(self):
        client = APIClient()
        # Login user
        client.login(username='user2', password='1234')
        # Put data
        data = {
            'title': 'New',
            'author': 1,
            'excerpt': 'New',
            'content': 'New',
            'status': 'published'
        }
        url = reverse('blog:post_details', kwargs={'pk': 1})
        response = client.put(url, data, format='json')
        # Assert
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


