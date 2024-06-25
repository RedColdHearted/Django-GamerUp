from rest_framework import status
from rest_framework.test import APITestCase

from django.urls import reverse

from posts.models import PostComment
from posts.serializers import PostCommentSerializer
from posts.tests.setup_fabric import SetUpFabric


class CommentsViewSetTests(APITestCase, SetUpFabric):
    def setUp(self):
        """set up for every test"""
        self.setup_users()
        self.setup_tokens()
        self.setup_posts()
        self.setup_comments()
        self.post2.refresh_from_db()

        self.create_url = reverse('comments-list')
        self.comment1_detail_url = reverse('comments-detail', kwargs={'pk': self.comment1.pk})

        self.comment2_detail_url = reverse('comments-detail', kwargs={'pk': self.comment2.pk})
        self.get_by_user1_url = reverse('comments-get-by-post', kwargs={'pk': self.user1.pk})
        self.get_by_user2_url = reverse('comments-get-by-post', kwargs={'pk': self.user2.pk})
        self.like1_url = reverse('comments-like', kwargs={'pk': self.comment1.pk})
        self.like2_url = reverse('comments-like', kwargs={'pk': self.comment2.pk})
        self.views1_url = reverse('comments-views-counter', kwargs={'pk': self.comment1.pk})
        self.views2_url = reverse('comments-views-counter', kwargs={'pk': self.comment2.pk})

    def test_adetail(self):
        """test: get comment1 by id"""
        response = self.client.get(self.comment1_detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK,)
        self.assertDictEqual(response.data, PostCommentSerializer(self.comment1).data)

    def test_create(self):
        """test: creating comment as user1 for post1"""
        self.user1.in_test_api_auth(self.client, self.token1)
        data = {'user': 1, 'user_post': self.post1.id, 'like_counter': 100, 'content': 'some_content'}
        response = self.client.post(self.create_url, data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED, response.data)
        self.assertEqual(PostComment.objects.count(), 3)

    def test_update(self):
        """test: updating user's comment"""
        # user1
        self.user1.in_test_api_auth(self.client, self.token1)
        data = {'user': 1, 'user_post': self.post1.id, 'like_counter': 1000000, 'content': 'new_content'}
        response = self.client.put(self.comment1_detail_url, data)
        self.comment1.refresh_from_db()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.comment1.content, data['content'])
        self.assertEqual(self.comment1.like_counter, data['like_counter'])

        # user2
        self.user2.in_test_api_auth(self.client, self.token2)
        data = {'user': self.user2.id, 'title': 'updated title', 'content': 'updated content'}
        response = self.client.put(self.comment1_detail_url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    #
    # def test_delete(self):
    #     """test: deleting user's post"""
    #     # user2
    #     self.user2.in_test_api_auth(self.client, self.token2)
    #     response = self.client.delete(self.post1_detail_url)
    #     self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    #     self.assertEqual(Post.objects.count(), 2)
    #
    #     # user1
    #     self.user1.in_test_api_auth(self.client, self.token1)
    #     response = self.client.delete(self.post1_detail_url)
    #     self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
    #     self.assertEqual(Post.objects.count(), 1)
    #
    # def test_get_by_user(self):
    #     """test: get all user's posts"""
    #     # user1
    #     response = self.client.get(self.get_by_user1_url)
    #     self.assertEqual(len(response.data), 1)
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)
    #
    #     # user2
    #     response = self.client.get(self.get_by_user2_url)
    #     self.assertEqual(len(response.data), 1)
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)
    #
    # def test_like(self):
    #     """test: post liking"""
    #     # user1
    #     self.user1.in_test_api_auth(self.client, self.token1)
    #     response = self.client.post(self.like1_url)
    #     self.post1.refresh_from_db()
    #     self.assertEqual(response.data['like_counter'], self.post1.like_counter)
    #
    #     # user2
    #     self.user2.in_test_api_auth(self.client, self.token2)
    #     response = self.client.post(self.like1_url)
    #     self.post1.refresh_from_db()
    #     self.assertEqual(response.data['like_counter'], self.post1.like_counter)
    #
    #     self.assertIn(self.user1, self.post1.liked_by.all())
    #     self.assertIn(self.user2, self.post1.liked_by.all())
    #
    # def test_views_counter(self):
    #     """test: post viewing"""
    #     # user1
    #     self.user1.in_test_api_auth(self.client, self.token1)
    #     self.client.post(self.views1_url)
    #
    #     # user 2
    #     self.user2.in_test_api_auth(self.client, self.token2)
    #     self.client.post(self.views2_url)
    #
    #     self.post1.refresh_from_db()
    #     self.post2.refresh_from_db()
    #
    #     self.assertEqual(self.post1.views, 1)
    #     self.assertEqual(self.post2.views, 1)
