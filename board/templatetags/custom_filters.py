from django import template
from django.utils import timezone

register = template.Library()


@register.filter
def custom_time(value):
    if not value:
        return ""

    now = timezone.localtime()
    value = timezone.localtime(value)

    if value.date() == now.date():
        # 오늘이면 "오전/오후 시:분"
        return value.strftime("%p %I:%M").replace("AM", "오전").replace("PM", "오후")
    elif value.year == now.year:
        # 올해면 "월.일 오전/오후 시:분"
        return (
            value.strftime("%m.%d %p %I:%M").replace("AM", "오전").replace("PM", "오후")
        )
    else:
        # 그 외는 "연.월.일 오전/오후 시:분"
        return (
            value.strftime("%Y.%m.%d %p %I:%M")
            .replace("AM", "오전")
            .replace("PM", "오후")
        )


@register.filter
def get_item(dictionary, key):
    # 딕셔너리에서 key에 해당하는 값을 가져온다.
    return dictionary.get(key)
