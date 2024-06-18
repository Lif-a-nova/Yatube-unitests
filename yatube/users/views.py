# Функция reverse_lazy позволяет получить URL по параметрам функции path()
from django.urls import reverse_lazy
from django.views.generic import CreateView

from .forms import CreationForm


class SignUp(CreateView):
    form_class = CreationForm
    success_url = reverse_lazy('posts:index')
    # После успешной регистрации перенаправляем пользователя на главную.
    template_name = 'users/signup.html'
    # имя шаблона, куда будет передана переменная form с объектом HTML-формы.
