# будет код фильтра, который даст возможность
# указывать CSS-класс в HTML-коде любого поля формы.
from django import template

register = template.Library()


@register.filter
def addclass(field, css):
    return field.as_widget(attrs={'class': css})
# синтаксис @register -
# это применение "декораторов", функций, меняющих поведение функций
