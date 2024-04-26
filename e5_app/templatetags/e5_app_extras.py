from django import template

register = template.Library()


@register.inclusion_tag('list.html')
def show_list(paragraph):
    lst = paragraph.split('\n')
    return {'lst': lst}


@register.inclusion_tag('directions_tag.html')
def directions_tag(start, end, alt, src):
    counts = map(str, list(range(start, end)))
    return {'counts': counts, 'alt': alt, 'src': src}


@register.inclusion_tag('history_indicator_tag.html')
def history_indicator_tag(start, end, target):
    counts = range(start, end)
    return {'counts': counts, 'target': target}


@register.inclusion_tag('history_inner_tag.html')
def history_inner_tag(start, end, alt, src):
    counts = map(str, list(range(start, end)))
    return {'counts': counts, 'alt': alt, 'src': src}
