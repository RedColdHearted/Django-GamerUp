from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import RefreshToken

from accounts.models import UserAccount
from posts.models import Post
from posts.serializers import PostSerializer


class PostViewSetTests(APITestCase):
    def setUp(self):
        self.user1 = UserAccount(
            username='username1',
            email='a@a.com',
            name='name1',
            password='password123',
            is_active=True,
        )
        self.user2 = UserAccount(
            username='username2',
            email='b@b.com',
            name='name2',
            password='password123',
            is_active=True,
        )
        self.user1.save()
        self.user2.save()
        self.user1_jwt = ''
        self.post1 = Post.objects.create(
            user=self.user1,
            title='title',
            content='content',
            views=123,
            like_counter=123,
        )
        self.post2 = Post.objects.create(
            user=self.user2,
            title='testing',
            content='testing',
            views=321,
            like_counter=321,
        )
        self.list_url = reverse('posts-list')
        self.post1_detail_url = reverse('posts-detail', kwargs={'pk': self.post1.pk})
        self.post2_detail_url = reverse('posts-detail', kwargs={'pk': self.post2.pk})
        self.get_by_user1_url = reverse('posts-get-by-user', kwargs={'pk': self.user1.pk})
        self.get_by_user2_url = reverse('posts-get-by-user', kwargs={'pk': self.user2.pk})
        self.like1_url = reverse('posts-like', kwargs={'pk': self.post1.pk})
        self.like2_url = reverse('posts-like', kwargs={'pk': self.post2.pk})
        self.token1 = self.get_jwt_token_for_user(self.user1)
        self.token2 = self.get_jwt_token_for_user(self.user2)

    @staticmethod
    def get_jwt_token_for_user(user):
        refresh = RefreshToken.for_user(user)
        return str(refresh.access_token)

    def api_authentication(self, token):
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + token)

    def like_post(self, token, like_url, total_likes, post, unlike=False):
        self.api_authentication(token)
        response = self.client.post(like_url)
        message = 'like removed' if unlike else 'liked'
        like_counter = total_likes - 1 if unlike else total_likes + 1
        self.assertEqual(response.data['status'], 'success')
        self.assertEqual(response.data['message'], message)
        self.assertEqual(response.data['like_counter'], like_counter)
        post.refresh_from_db()

    def complete_like_post(self, token, user, like_url, post, ):
        self.like_post(token, like_url, post.like_counter, post)
        self.assertTrue(post.liked_by.filter(pk=user.pk).exists())
        self.assertIn(user, post.liked_by.all())
        self.like_post(token, like_url, post.like_counter, post, unlike=True)
        self.assertFalse(post.liked_by.filter(pk=user.pk).exists())
        self.assertNotIn(user, post.liked_by.all())

    def test_list_posts(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 4)

    def test_detail_post(self):
        response = self.client.get(self.post1_detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertDictEqual(response.data, PostSerializer(self.post1).data)

    def test_create_post(self):
        self.api_authentication(self.token1)
        data = {'user': 1, 'title': 'some_title', 'content': 'some_content'}
        response = self.client.post(self.list_url, data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Post.objects.count(), 3)

    def test_update_post(self):
        # user1
        self.api_authentication(self.token1)
        data = {'user': self.user1.id, 'title': 'updated title', 'content': 'updated content'}
        response = self.client.put(self.post1_detail_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.post1.refresh_from_db()
        self.assertEqual(self.post1.title, data['title'])
        self.assertEqual(self.post1.content, data['content'])

        # user2
        self.api_authentication(self.token2)
        data = {'user': self.user2.id, 'title': 'updated title', 'content': 'updated content'}
        response = self.client.put(self.post1_detail_url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_posts(self):
        # user2
        self.api_authentication(self.token2)
        response = self.client.delete(self.post1_detail_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Post.objects.count(), 2)

        # user1
        self.api_authentication(self.token1)
        response = self.client.delete(self.post1_detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Post.objects.count(), 1)

    def test_get_by_user_posts(self):
        # user1
        response = self.client.get(self.get_by_user1_url)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # user2
        response = self.client.get(self.get_by_user2_url)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_like_posts(self):
        # post1
        self.complete_like_post(self.token1, self.user1, self.like1_url, self.post1)
        self.complete_like_post(self.token2, self.user2, self.like1_url, self.post1)

        # post2
        self.complete_like_post(self.token1, self.user1, self.like2_url, self.post2)
        self.complete_like_post(self.token2, self.user2, self.like2_url, self.post2)

        # user1, user2 in many-to-many field

        self.api_authentication(self.token1)
        response = self.client.post(self.like1_url)
        self.post1.refresh_from_db()
        self.api_authentication(self.token2)
        response = self.client.post(self.like1_url)
        self.post1.refresh_from_db()
        self.assertIn(self.user1, self.post1.liked_by.all())
        self.assertIn(self.user2, self.post1.liked_by.all())

        self.api_authentication(self.token1)
        response = self.client.post(self.like1_url)
        self.post1.refresh_from_db()
        self.api_authentication(self.token2)
        response = self.client.post(self.like1_url)
        self.post1.refresh_from_db()
        self.assertNotIn(self.user1, self.post1.liked_by.all())
        self.assertNotIn(self.user2, self.post1.liked_by.all())
