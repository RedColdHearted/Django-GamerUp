from rest_framework import status
from rest_framework.test import APITestCase

from django.urls import reverse

from posts.models import Post
from posts.serializers import PostSerializer
from posts.tests.setup_fabric import SetUpFabric


class PostViewSetTests(APITestCase, SetUpFabric):
    def setUp(self):
        """set up for every test"""
        self.setup_users()
        self.setup_posts()
        self.setup_tokens()

        self.list_url = reverse('posts-list')
        self.post1_detail_url = reverse('posts-detail', kwargs={'pk': self.post1.pk})
        self.post2_detail_url = reverse('posts-detail', kwargs={'pk': self.post2.pk})
        self.get_by_user1_url = reverse('posts-get-by-user', kwargs={'pk': self.user1.pk})
        self.get_by_user2_url = reverse('posts-get-by-user', kwargs={'pk': self.user2.pk})
        self.like1_url = reverse('posts-like', kwargs={'pk': self.post1.pk})
        self.like2_url = reverse('posts-like', kwargs={'pk': self.post2.pk})
        self.views1_url = reverse('posts-views-counter', kwargs={'pk': self.post1.pk})
        self.views2_url = reverse('posts-views-counter', kwargs={'pk': self.post2.pk})

    def test_list_posts(self):
        """test: get all posts"""
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 4)

    def test_detail_posts(self):
        """test: get post1 by id"""
        response = self.client.get(self.post1_detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertDictEqual(response.data, PostSerializer(self.post1).data)

    def test_create_posts(self):
        """test: creating post as user1"""
        self.user1.in_test_api_auth(self.client, self.token1)
        data = {'user': 1, 'title': 'some_title', 'content': 'some_content'}
        response = self.client.post(self.list_url, data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Post.objects.count(), 3)

    def test_update_posts(self):
        """test: updating user's post"""
        # user1
        self.user1.in_test_api_auth(self.client, self.token1)
        data = {'user': self.user1.id, 'title': 'updated title', 'content': 'updated content'}
        response = self.client.put(self.post1_detail_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.post1.refresh_from_db()
        self.assertEqual(self.post1.title, data['title'])
        self.assertEqual(self.post1.content, data['content'])

        # user2
        self.user2.in_test_api_auth(self.client, self.token2)
        data = {'user': self.user2.id, 'title': 'updated title', 'content': 'updated content'}
        response = self.client.put(self.post1_detail_url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_posts(self):
        """test: deleting user's post"""
        # user2
        self.user2.in_test_api_auth(self.client, self.token2)
        response = self.client.delete(self.post1_detail_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Post.objects.count(), 2)

        # user1
        self.user1.in_test_api_auth(self.client, self.token1)
        response = self.client.delete(self.post1_detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Post.objects.count(), 1)

    def test_get_by_user_posts(self):
        """test: get all user's posts"""
        # user1
        response = self.client.get(self.get_by_user1_url)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # user2
        response = self.client.get(self.get_by_user2_url)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_like_posts(self):
        """test: post liking"""
        # user1
        self.user1.in_test_api_auth(self.client, self.token1)
        response = self.client.post(self.like1_url)
        self.post1.refresh_from_db()
        self.assertEqual(response.data['like_counter'], self.post1.like_counter)

        # user2
        self.user2.in_test_api_auth(self.client, self.token2)
        response = self.client.post(self.like1_url)
        self.post1.refresh_from_db()
        self.assertEqual(response.data['like_counter'], self.post1.like_counter)

        self.assertIn(self.user1, self.post1.liked_by.all())
        self.assertIn(self.user2, self.post1.liked_by.all())

    def test_views_counter_posts(self):
        """test: post viewing"""
        # user1
        self.user1.in_test_api_auth(self.client, self.token1)
        self.client.post(self.views1_url)

        # user 2
        self.user2.in_test_api_auth(self.client, self.token2)
        self.client.post(self.views2_url)

        self.post1.refresh_from_db()
        self.post2.refresh_from_db()

        self.assertEqual(self.post1.views, 1)
        self.assertEqual(self.post2.views, 1)
