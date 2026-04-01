from fashionWebsite.clothes.models import Category, Color, Size


def global_filters(request):
    return {
        'categories': Category.objects.all(),
        'colors': Color.objects.all(),
        'sizes': Size.objects.all(),
    }