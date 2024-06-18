from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse

from posts.forms import PostForm
from posts.models import Group, Post

User = get_user_model()


class PostPagesTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='User')
        cls.user_2 = User.objects.create_user(username='User-2')
        cls.group = Group.objects.create(
            title='Тестовая группа',
            slug='test-slug',
            description='Тестовое описание Группы',
        )
        cls.group_2 = Group.objects.create(slug='test-slug-2')
        cls.post = Post.objects.create(
            text='Тестовый первый новый пост',
            author=cls.user,
            group=cls.group,
        )

    def setUp(self):
        self.guest_client = Client()
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)

    def obj_context(self, checked_obj):
        compare_names = {
            checked_obj.id: self.post.id,
            checked_obj.text: self.post.text,
            checked_obj.author: self.post.author,
            checked_obj.group: self.post.group,
        }
        for object, expected_obj in compare_names.items():
            with self.subTest(object=object):
                self.assertEqual(object, expected_obj)

    def test_pages_uses_correct_template(self):
        """URL-адрес использует соответствующий шаблон."""
        templates_pages_names = {
            reverse('posts:index'): 'posts/index.html',
            (reverse(
                'posts:group_list',
                kwargs={'slug': self.post.group.slug}
            )
            ): 'posts/group_list.html',
            (reverse(
                'posts:profile',
                kwargs={'username': self.post.author.username}
            )
            ): 'posts/profile.html',
            (reverse(
                'posts:post_detail',
                kwargs={'post_id': self.post.id}
            )
            ): 'posts/post_detail.html',
            (reverse(
                'posts:post_edit',
                kwargs={'post_id': self.post.id}
            )
            ): 'posts/create_post.html',
            reverse('posts:post_create'): 'posts/create_post.html',
        }
        for reverse_name, template in templates_pages_names.items():
            with self.subTest(reverse_name=reverse_name):
                response = self.authorized_client.get(reverse_name)
                self.assertTemplateUsed(response, template)

    def test_create_edit_post_is_correct_form(self):
        """Шаблоны create, edit_post нужной формы."""
        is_form = {
            reverse('posts:post_create'): None,
            reverse(
                'posts:post_edit', kwargs={'post_id': self.post.id}
            ): True
        }
        for reverse_name, is_edit_is in is_form.items():
            with self.subTest(reverse_name=reverse_name):
                response = self.authorized_client.get(reverse_name)
                form = response.context.get('form')
                self.assertIsInstance(form, PostForm)
                is_edit = response.context.get('is_edit')
                self.assertEqual(is_edit, is_edit_is)

    def test_post_detail_pages_show_correct_context(self):
        """Шаблон post_detail сформирован с правильным контекстом."""
        response = self.authorized_client.get(
            reverse('posts:post_detail', kwargs={'post_id': self.post.id})
        )
        checked_obj = response.context.get('post')
        self.obj_context(checked_obj)
        checked_post_count = response.context.get('post_count')
        self.assertEqual(checked_post_count, 1)

    def test_index_show_correct_context(self):
        """Пост появляется Первым на стр index c правильным контекстом."""
        response = self.authorized_client.get(reverse('posts:index'))
        checked_obj = response.context['page_obj'][0]
        self.obj_context(checked_obj)

    def test_profile_show_correct_context(self):
        """Пост появляется Первым на стр profile c правильным контекстом."""
        response = self.authorized_client.get(
            reverse('posts:profile', kwargs={'username': self.user.username})
        )
        checked_obj = response.context['page_obj'][0]
        self.obj_context(checked_obj)
        checked_post_count = response.context.get('post_count')
        self.assertEqual(checked_post_count, 1)
        checked_author = response.context.get('author')
        self.assertEqual(checked_author, self.post.author)

    def test_group_list_show_correct_context(self):
        """Пост появляется Первым на стр group_list c правильным контекстом."""
        response = self.authorized_client.get(
            reverse('posts:group_list', kwargs={'slug': self.group.slug})
        )
        checked_obj = response.context['page_obj'][0]
        self.obj_context(checked_obj)
        checked_group = response.context.get('group')
        self.assertEqual(checked_group.description,
                         self.post.group.description)
        self.assertEqual(checked_group.title, self.post.group.title)

    def test_post_not_in_pages(self):
        """Пост НЕ появляется где не надо."""
        self.post_2 = Post.objects.create(
            text='Тестовый третий пост',
            author=self.user,
            group=self.group_2,
        )
        pages = (
            reverse('posts:profile',
                    kwargs={'username': self.user_2.username}),
            reverse('posts:group_list',
                    kwargs={'slug': self.group.slug}),
        )
        for reverse_name in pages:
            with self.subTest(reverse_name=reverse_name):
                response = self.authorized_client.get(reverse_name)
                checked_obj = response.context['page_obj']
                self.assertNotIn(self.post_2, checked_obj)
