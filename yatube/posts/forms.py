from django import forms

from .models import Post


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('text', 'group')
        help_texts = {
            'text': 'Текст нового поста',
            'group': 'Группа, к которой будет относиться пост. Необязательно'
        }
        labels = {
            'text': 'Постик',
            'group': 'Группчка'
        }

    def clean_text(self):
        data = self.cleaned_data['text']
        if data.lower() is None:
            raise forms.ValidationError
        return data
