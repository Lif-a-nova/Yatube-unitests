from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.paginator import Page
from django.test import Client, TestCase
from django.urls import reverse

from posts.models import Group, Post

User = get_user_model()


PLUS_POST: int = 3


class PaginatorViewsTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='User')
        cls.group = Group.objects.create(slug='test-slug')
        Post.objects.bulk_create(
            [
                Post(text="Тестовый пост",
                     group=cls.group,
                     author=cls.user,
                     )
                for _ in range(settings.POSTS_PER_PAGE + PLUS_POST)
            ]
        )

    def setUp(self):
        self.client = Client()

    def test_paginator(self):
        views = {
            reverse('posts:index'),
            reverse('posts:group_list',
                    kwargs={'slug': self.group.slug}),
            reverse('posts:profile',
                    kwargs={'username': self.user.username})
        }
        for view in views:
            for page_s in (1, 2):
                with self.subTest(page_s=page_s):
                    response = self.client.get(view, [('page', page_s)])
                    self.assertIn('page_obj', response.context)
                    page: Page = response.context['page_obj']
                    if page_s == 1:
                        self.assertEqual(len(page.object_list),
                                         settings.POSTS_PER_PAGE)
                    else:
                        self.assertEqual(len(page.object_list), PLUS_POST)
