# your_app/templatetags/menu_tags.py

from django import template
from django.urls import resolve

register = template.Library()

@register.simple_tag(takes_context=True)
def active(context, url_name, identifier=None, root_path=False):
    request = context['request']
    try:
        current_url_name = resolve(request.path_info).url_name
    except:
        current_url_name = None
    current_path = request.path

    if root_path and current_path == '/':
        return "active"

    if identifier:
        return "active" if current_url_name == url_name and identifier in current_path else ""
    return "active" if current_url_name == url_name else ""

@register.simple_tag(takes_context=True)
def menu_active(context, *url_names):
    """
    Kthen 'here show' nëse URL e tanishme është në url_names, përndryshe ''
    """
    request = context.get('request')
    if not request:
        return ''

    try:
        current_url_name = resolve(request.path_info).url_name
    except:
        current_url_name = None

    if current_url_name in url_names:
        return 'here show'
    return ''
