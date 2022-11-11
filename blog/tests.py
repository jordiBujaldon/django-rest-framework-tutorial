from blog.models import Category, Post

from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient, APITestCase

from users.models import CustomUser


class TestPostModel(TestCase):
    @classmethod
    def setUpTestData(cls):
        Category.objects.create(name='django')
        CustomUser.objects.create_user(email='user@user.com', user_name='user', first_name='', password='1234')
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
        CustomUser.objects.create_user(email='user@user.com', user_name='user', first_name='', password='1234')
        CustomUser.objects.create_user(email='user2@user.com', user_name='user2', first_name='', password='1234')
        Post.objects.create(title='Post title', excerpt='Post excerpt', content='Post content', slug='post-title',
                            status='published', category_id=1, author_id=1)

    def test_get_post_list(self):
        url = reverse('blog:post_list')
        response = self.client.get(url, format='json')
        # Assert status
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_post_post(self):
        # Login
        url_post_login = reverse('token_obtain_pair')
        login_data = {
            'user_name': 'user',
            'password': '1234'
        }
        response = self.client.post(url_post_login, login_data, format='json')
        # Asserts
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue('access' in response.data)
        # Set token to client
        token = response.data['access']
        self.client.credentials(HTTP_AUTHORIZATION='JWT {}'.format(token))
        # Post data
        data = {
            'title': 'Post title',
            'excerpt': 'Post excerpt',
            'content': 'Post content',
            'author': 1
        }
        url = reverse('blog:post_list')
        response = self.client.post(url, data, format='json')
        # Assert
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get_post_detail(self):
        # Login
        url_post_login = reverse('token_obtain_pair')
        login_data = {
            'user_name': 'user',
            'password': '1234'
        }
        response = self.client.post(url_post_login, login_data, format='json')
        # Asserts
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue('access' in response.data)
        # Set token to client
        token = response.data['access']
        self.client.credentials(HTTP_AUTHORIZATION='JWT {}'.format(token))
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
        # Login
        client = APIClient()
        url_post_login = reverse('token_obtain_pair')
        login_data = {
            'user_name': 'user',
            'password': '1234'
        }
        response = client.post(url_post_login, login_data, format='json')
        # Asserts
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue('access' in response.data)
        # Set token to client
        token = response.data['access']
        client.credentials(HTTP_AUTHORIZATION='JWT {}'.format(token))
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
        self.assertEqual(response.status_code, status.HTTP_200_OK)
