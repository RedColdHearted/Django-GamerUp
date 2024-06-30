import os

from rest_framework import status
from rest_framework.test import APITestCase

from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile

from accounts.serializers import CustomUserCreateSerializer
from app.utils import is_not_default_pic
from posts.tests.setup_fabric import SetUpFabric


class UsersViewSetTests(APITestCase, SetUpFabric):
    def setUp(self):
        """set up for every test"""
        self.setup_users()
        self.setup_tokens()

        self.user1_detail_url = reverse('users-detail', kwargs={'pk': self.user1.pk})
        self.user2_detail_url = reverse('users-detail', kwargs={'pk': self.user2.pk})

        self.user1_change_username_url = reverse('users-change-username', kwargs={'pk': self.user1.pk})
        self.user2_change_username_url = reverse('users-change-username', kwargs={'pk': self.user2.pk})

        self.user1_change_avatar_url = reverse('users-change-avatar', kwargs={'pk': self.user1.pk})
        self.user2_change_avatar_url = reverse('users-change-avatar', kwargs={'pk': self.user2.pk})

    def test_detail(self):
        """test: get users by id"""
        response = self.client.get(self.user1_detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK,)
        self.assertDictEqual(response.data, CustomUserCreateSerializer(self.user1).data)

        response = self.client.get(self.user2_detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK, )
        self.assertDictEqual(response.data, CustomUserCreateSerializer(self.user2).data)

    def test_change_username(self):
        """test: change username"""
        # user1
        self.user1.in_test_api_auth(self.client, self.token1)
        data1 = {'username': 'noob1337'}
        response = self.client.post(self.user1_change_username_url, data=data1)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # user2
        self.user2.in_test_api_auth(self.client, self.token2)
        data2 = {'username': 'noob2284'}
        response = self.client.post(self.user2_change_username_url, data=data2)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.user1.refresh_from_db()
        self.user2.refresh_from_db()
        self.assertEqual(self.user1.username, data1['username'])
        self.assertEqual(self.user2.username, data2['username'])

        self.user1.in_test_api_auth(self.client, self.token1)
        response = self.client.post(self.user2_change_username_url, data=data1)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        self.user2.in_test_api_auth(self.client, self.token2)
        response = self.client.post(self.user1_change_username_url, data=data2)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_change_avatar(self):
        """test: upload user's avatar trough api"""
        image_path = os.path.join(os.path.dirname(__file__), 'files', 'test_image.jpg')

        with open(image_path, 'rb') as img:
            image_data = img.read()
            uploaded_image = SimpleUploadedFile('test_image.png', image_data, content_type='image/jpg')
            data = {'avatar': uploaded_image}

            # user1
            self.user1.in_test_api_auth(self.client, self.token1)
            response = self.client.post(self.user1_change_avatar_url, data, format='multipart')
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)

            # user2
            self.user1.in_test_api_auth(self.client, self.token1)
            response = self.client.post(self.user2_change_avatar_url, data, format='multipart')
            self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

            self.user1.refresh_from_db()
            temp_path = self.user1.image.path
            if is_not_default_pic(temp_path):
                os.remove(temp_path)
