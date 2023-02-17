from django import template


register = template.Library()



# Регистрируем наш фильтр под именем currency, чтоб Django понимал,
# что это именно фильтр для шаблонов, а не простая функция.
@register.filter()
def censor(value):
    try:
        if "редиска" in value:
            value = value.replace('редиска', 'р******')
            return value
        else:
            return value
    except:
        raise TypeError("Функция принимает только строки")
