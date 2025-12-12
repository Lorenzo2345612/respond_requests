"""
Template tags personalizados para la app tipo_solicitudes
Archivo: tipo_solicitudes/templatetags/extra_filters.py
"""
from django import template

register = template.Library()


@register.filter(name='get_item')
def get_item(dictionary, key):
    """
    Permite acceder a un diccionario usando una clave dinámica en templates
    Uso: {{ mi_dict|get_item:clave_variable }}
    """
    if dictionary is None:
        return None
    return dictionary.get(key, '')


@register.filter(name='split')
def split(value, arg):
    """
    Divide una cadena usando el separador especificado
    Uso: {{ "a,b,c"|split:"," }}
    Retorna lista vacía si el valor es None
    """
    if value is None:
        return []
    return [item.strip() for item in value.split(arg)]
