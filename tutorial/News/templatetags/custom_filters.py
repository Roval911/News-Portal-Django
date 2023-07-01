from django import template
register = template.Library()


stop_words = [
    'слово1',
    'слово2',
    'слово3',
]


@register.filter(name='censor')
def censor(value):
    for i in stop_words:
        value = value.lower().replace(i.lower(), '***')
    return value