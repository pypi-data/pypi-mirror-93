from django import template
from yum.models import MenuItem
from django.urls import reverse, NoReverseMatch


register = template.Library()

def into_tree(parent, children_by_parent,code): #функция, которая берёт родителя и смотрит  есть ли у него дети, если есть она идёт в глубь и спрашивает у следующего сына.
    if parent.id in children_by_parent and parent.active is True:
        code.append('<ul>')
        for m in children_by_parent[parent.id]:
            code.append('<li>')
            code.append(f"<a href='{m.url}'>{m.title}</a>")
            into_tree(m, children_by_parent, code)
            code.append('</li>')
        code.append('</ul>')
    else:
        return

def try_reverse(url):
    try:
        return reverse(url)
    except NoReverseMatch:
        return url



@register.inclusion_tag('yum/menu.html')
def draw_menu(name, active_path):
    menu = MenuItem.objects.filter(name = name)
    children_by_parent = {}
    root_child = None
    for m in menu:
        m.active = False
        m.url = try_reverse(m.url)
        if m.url == active_path:
            m.active = True
            root_child = m
        if m.parent_id not in children_by_parent:
            children_by_parent[m.parent_id] = [m]
        else:
            children_by_parent[m.parent_id].append(m)

    if active_path != '/': #если юрл пустой
        while root_child.parent_id != None:
            for m in menu:
                if root_child.parent_id == m.id:
                    root_child = m
                    root_child.active = True

    result = []
    result.append('<ul>')
    for m in children_by_parent[None]:
        result.append('<li>')
        result.append(f"<a href='{m.url}'>{m.title}</a>")
        into_tree(m, children_by_parent, result)
        result.append('</li>')
    result.append('</ul>')
    return {'menu': result}
