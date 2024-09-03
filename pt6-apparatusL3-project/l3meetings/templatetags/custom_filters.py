from django import template

register = template.Library()
import urllib.parse


@register.filter(name='string_replace')
def string_replace(value, arg):
    return value.replace(arg.split(',')[0], arg.split(',')[1])

@register.filter(name='url_decode')
def url_decode(value):
    decoded_url = urllib.parse.unquote(value)
    if decoded_url.startswith('/https:/'):
        decoded_url = decoded_url[1:]
    return decoded_url.replace("https:/", "https://")


@register.filter(name='in_groups')
def in_groups(user, group_names):
    group_list = group_names.split(',')
    return user.groups.filter(name__in=group_list).exists()