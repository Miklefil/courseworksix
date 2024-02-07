from django import template

register = template.Library()


@register.filter()
def blog_preview(val):
    if val:
        return f'/media/{val}'

    return '#'