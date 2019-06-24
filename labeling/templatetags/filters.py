from django import template
import json
register = template.Library()

@register.filter
def hash(h, key):
    #return h[key]
    return h.get(key, None)

@register.filter
def as_json(data):
    return json.dumps(data)
