from http import HTTPStatus

from django.contrib.auth import get_user_model
from django.test import Client, TestCase

from posts.models import Group, Post

User = get_user_model()


class PostURLTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user_aut = User.objects.create_user(username='Author')
        cls.user_ano = User.objects.create_user(username='Another')
        cls.group = Group.objects.create(slug='test-slug')
        cls.post = Post.objects.create(
            text='Тестовый длииииинный пост',
            author=cls.user_aut,
            group=cls.group,
        )

    def setUp(self):
        self.guest_client = Client()
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user_ano)
        self.authorized_author = Client()
        self.authorized_author.force_login(self.user_aut)

    def test_urls_uses_correct_template(self):
        """URL-адрес использует соответствующий шаблон"""
        templates_url_names = {
            '/': 'posts/index.html',
            f'/group/{self.group.slug}/': 'posts/group_list.html',
            f'/profile/{self.post.author.username}/': 'posts/profile.html',
            f'/posts/{self.post.id}/': 'posts/post_detail.html',
            '/create/': 'posts/create_post.html',
            f'/posts/{self.post.id}/edit/': 'posts/create_post.html',
        }
        for address, template in templates_url_names.items():
            with self.subTest(address=address):
                response = self.authorized_author.get(address)
                self.assertTemplateUsed(response, template)

    def test_urls_for_author(self):
        """Доступность страниц только для автора."""
        response = self.authorized_client.get(
            f'/posts/{self.post.id}/edit/', follow=True)
        self.assertRedirects(
            response, f'/posts/{self.post.id}/')

    def test_urls_for_user(self):
        """Доступность страниц для автора."""
        response = self.authorized_author.get('/create/')
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_url_for_author(self):
        """Доступность страниц для пользователя."""
        response = self.authorized_author.get(
            f'/posts/{self.post.id}/edit/'
        )
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_url_http_status(self):
        """HTTPStatus страниц для любого пользователя."""
        url_http_status = {
            '/': HTTPStatus.OK,
            f'/group/{self.group.slug}/': HTTPStatus.OK,
            f'/profile/{self.post.author.username}/': HTTPStatus.OK,
            f'/posts/{self.post.id}/': HTTPStatus.OK,
            # '/unexisting_page/': HTTPStatus.NOT_FOUND  не рб на спринте 6
        }
        for address, expected_status in url_http_status.items():
            with self.subTest(address=address):
                response = self.guest_client.get(address)
                self.assertEqual(response.status_code, expected_status)

    def test_urls_redirect_anonymous_on_auth_login(self):
        """Редирект для неавторизованного пользователя."""
        urls = (
            '/create/',
            f'/posts/{self.post.id}/edit/',
        )
        for url in urls:
            response = self.guest_client.get(url, follow=True)
            self.assertRedirects(
                response, f'/auth/login/?next={url}')
