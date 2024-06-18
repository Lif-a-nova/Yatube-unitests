from django.contrib.auth import get_user_model
from django.test import TestCase

from ..models import Group, Post

User = get_user_model()

CROP_TEXT: int = 15


class PostModelTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='User')
        cls.group = Group.objects.create(
            title='Тестовая группа',
            slug='test-slug',
            description='Тестовое описание Группы',
        )
        cls.post = Post.objects.create(
            text='Тестовый длииииинный пост',
            author=cls.user,
            group=cls.group,
        )

    def test_models_post_have_correct_str_text(self):
        """__str__ Post-модели возвращает обрезаный текст."""
        post = PostModelTest.post
        expected_object_name = post.text[:CROP_TEXT]
        self.assertEqual(expected_object_name, str(post))

    def test_models_group_have_correct_str_title(self):
        """__str__ Group-модели возвращает название группы."""
        group = PostModelTest.group
        expected_object_name = group.title
        self.assertEqual(expected_object_name, str(group))
