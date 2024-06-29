from datetime import datetime

import pytz

from django.utils import timezone

from accounts.models import UserAccount
from app.exceptions import CommentTestCaseException, PostTestCaseException, TokenTestCaseException
from posts.models import Post, Comment


class SetUpFabric:
    aware_datetime = timezone.make_aware(datetime(year=2000, day=1, month=1), pytz.UTC)

    def _hasattrs(self, name1: str, name2: str) -> bool:
        """This function need to check attrs before setup"""
        return hasattr(self, name1) and hasattr(self, name2)

    def setup_users(self):
        """set up users for every test"""
        self.user1 = UserAccount(
            username='username1',
            email='a@a.com',
            name='name1',
            password='password123',
            is_active=True,
            username_last_updated_at=self.aware_datetime,
        )
        self.user2 = UserAccount(
            username='username2',
            email='b@b.com',
            name='name2',
            password='password123',
            is_active=True,
            username_last_updated_at=self.aware_datetime,
        )
        self.user1.save()
        self.user2.save()

    def setup_tokens(self):
        """set up user's jwt tokens for every test"""
        if self._hasattrs('user1', 'user2'):
            self.token1 = self.user1.get_jwt_token_for_user()
            self.token2 = self.user2.get_jwt_token_for_user()
        else:
            raise TokenTestCaseException('You need users to create tokens')

    def setup_posts(self):
        """set up posts for every test"""
        if self._hasattrs('user1', 'user2'):
            self.post1 = Post.objects.create(
                user=self.user1,
                title='title',
                content='content',
                views=0,
                like_counter=123,
            )
            self.post2 = Post.objects.create(
                user=self.user2,
                title='testing',
                content='testing',
                views=0,
                like_counter=321,
            )
        else:
            raise PostTestCaseException('You need users to create posts')

    def setup_comments(self):
        """set up comments for every test"""
        if self._hasattrs('post1', 'post2'):
            self.comment1 = Comment(
                user=self.post1.user,
                user_post=self.post1,
                content='test'
            )
            self.comment2 = Comment(
                user=self.post2.user,
                user_post=self.post2,
                content='test'
            )
            self.comment1.save()
            self.comment2.save()
        else:
            raise CommentTestCaseException('You need posts to create comments')
