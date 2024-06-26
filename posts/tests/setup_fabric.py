from accounts.models import UserAccount
from posts.models import Post, Comment


class SetUpFabric:
    def setup_users(self):
        """set up users for every test"""
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

    def setup_tokens(self):
        """set up user's jwt tokens for every test"""
        self.token1 = self.user1.get_jwt_token_for_user()
        self.token2 = self.user2.get_jwt_token_for_user()

    def setup_posts(self):
        """set up posts for every test"""
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

    def setup_comments(self):
        """set up comments for every test"""
        self.post1 = self.__dict__.get('post1')
        self.post2 = self.__dict__.get('post2')

        if self.post1 and self.post2:
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
