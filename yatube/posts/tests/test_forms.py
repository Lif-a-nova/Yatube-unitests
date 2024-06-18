from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse

from posts.forms import PostForm
from posts.models import Group, Post

User = get_user_model()


class PostFormTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='User')
        cls.user_2 = User.objects.create_user(username='User-2')
        cls.group = Group.objects.create(
            title='Первая группа',
            slug='test-slug',
            description='Описание первой Группы',
        )
        cls.group_2 = Group.objects.create(
            title='Воторая группа',
            slug='test-slug-2',
            description='Описание второй Группы',
        )
        cls.post = Post.objects.create(
            text='Тестовый пост',
            author=cls.user,
            group=cls.group,
        )
        cls.form = PostForm()

    def setUp(self):
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)

    def test_create_post_show_correct_context(self):
        """Проверка создания поста."""
        posts_count = Post.objects.count()
        form_data = {
            'text': 'Новый пост',
            'group': self.group.pk,
        }
        redirect = reverse('posts:profile', kwargs={
                           'username': self.user.username}
                           )
        response = self.authorized_client.post(
            reverse('posts:post_create'),
            data=form_data,
            follow=True
        )
        self.assertRedirects(response, redirect)
        self.assertEqual(Post.objects.count(), posts_count + 1)
        self.assertTrue(
            Post.objects.filter(
                text='Новый пост',
                group=self.group.pk,
                author=self.user
            ).exists()
        )

    def test_edit_post_show_correct_context(self):
        """Проверка редактирования поста."""
        form_data = {
            'text': 'Редактированный пост',
            'group': self.group_2.pk,
        }
        redirect = reverse('posts:post_detail',
                           kwargs={'post_id': self.post.id}
                           )
        response_edit = self.authorized_client.post(
            reverse('posts:post_edit', kwargs={'post_id': self.post.id}),
            data=form_data,
            follow=True
        )
        self.assertRedirects(response_edit, redirect)
        self.assertTrue(
            Post.objects.filter(
                text='Редактированный пост',
                group=self.group_2.pk,
                author=self.user,
                id=self.post.id
            ).exists()
        )

    def test_title_label(self):
        """Проверка генерации labels и help_text."""
        title_label = PostFormTests.form.fields['text'].label
        self.assertEqual(title_label, 'Постик')

    def test_title_help_text(self):
        title_help_text = PostFormTests.form.fields['text'].help_text
        self.assertEqual(title_help_text, 'Текст нового поста')
