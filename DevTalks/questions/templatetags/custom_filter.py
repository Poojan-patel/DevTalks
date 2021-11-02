from django import template

register = template.Library()

@register.filter(name="find_user")
def find_user(query_set, user):
    return query_set.filter(user=user).exists()
    # return True