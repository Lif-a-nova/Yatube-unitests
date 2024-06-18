from django.views.generic.base import TemplateView


class AboutAuthor(TemplateView):
    # В переменной template_name обязательно указывается имя шаблона,
    # на основе которого будет создана возвращаемая страница
    template_name = 'app_name/author.html'


class AboutTech(TemplateView):
    template_name = 'app_name/tech.html'
