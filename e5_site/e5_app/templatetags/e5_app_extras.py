from django import template

register = template.Library()


@register.inclusion_tag('list.html')
def show_list(paragraph):
    lst = paragraph.split('\n')
    return {'lst': lst}
