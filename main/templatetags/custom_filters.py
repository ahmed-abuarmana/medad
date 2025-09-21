from django import template

register = template.Library()

@register.filter
def arabic_time(value):
    if not value:
        return ""
    hour = value.strftime("%I")
    minute = value.strftime("%M")
    suffix = "صباحًا" if value.strftime("%p") == "AM" else "مساءً"
    return f"{hour}:{minute} {suffix}"
