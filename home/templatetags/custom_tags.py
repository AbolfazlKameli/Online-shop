import string

from django import template

register = template.Library()


@register.filter
def cap_all(value):
    return string.capwords(value)


@register.filter
def separate(value):
    value_str = str(value)
    length = len(value_str)
    if length % 3 == 0:
        parts = [value_str[i:i + 3] for i in range(0, length, 3)]
    else:
        first_part = value_str[:length % 3]
        parts = [first_part] + [value_str[i:i + 3] for i in range(length % 3, length, 3)]
    result = ",".join(parts)
    return result
