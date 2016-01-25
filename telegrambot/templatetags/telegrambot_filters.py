from django import template
from django.http import QueryDict
register = template.Library()

@register.filter(name='keyboard_field')
def keyboard_field(value, args=None):
    """
    Format keyboard /command field. 
    """
    qs = QueryDict(args)
    per_line = qs.get('per_line', 1)
    field = qs.get("field", "slug")
    command = qs.get("command")
    convert = lambda element: "/" + command + " " + str(getattr(element, field))
    group = lambda flat, size: [flat[i:i+size] for i in range(0, len(flat), size)]
    grouped = group(value, int(per_line))
    new_list = []
    for line in grouped:
        new_list.append([convert(e) for e in line])     
    return str(new_list).encode('utf-8')