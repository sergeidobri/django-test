from django import template
import nails.views as views
from nails.models import Category, TagPost
from django.db.models import Q, Count
from nails.utils import menu_lst

register = template.Library()


@register.simple_tag()
def get_menu():
    return menu_lst


@register.inclusion_tag('nails/list_categories.html')
def show_categories(cat_selected=0):
    cats = Category.objects.annotate(total=Count('types')).filter(~Q(total=0))
    return {'cats': cats, 'cat_selected': cat_selected}


@register.inclusion_tag('nails/list_tags.html')
def show_all_tags():
    return {'tags': TagPost.objects.annotate(total=Count('tags')).filter(~Q(total=0))}
