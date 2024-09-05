from django import template
from django.urls import resolve

register = template.Library()

@register.simple_tag(takes_context=True)
def active(context, url_name, identifier=None, root_path=False):
    request = context['request']
    current_url_name = resolve(request.path_info).url_name
    current_path = request.path

    # Handling root URL specifically
    if root_path and current_path == '/':
        return "active"

    if identifier:
        return "active" if current_url_name == url_name and identifier in current_path else ""
    return "active" if current_url_name == url_name else ""
