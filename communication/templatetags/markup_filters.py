'''This package has the template filters for the communication app.

Currently there is just a markdown filter for converting RST into HTML files.'''

from docutils.core import publish_parts

from django import template
from django.template.defaultfilters import stringfilter

register = template.Library()

@register.filter(is_safe=True)
@stringfilter
def markdown_rst(value):
    return publish_parts(value, writer_name='html')['html_body']

register.filter('markdown_rst', markdown_rst)

