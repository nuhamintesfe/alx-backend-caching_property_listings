from django.shortcuts import render
from django.views.decorators.cache import cache_page
from .utils import get_all_properties

@cache_page(60 * 15)  # Cache the entire view response for 15 minutes
def property_list(request):
    properties = get_all_properties()  # Cached queryset for 1 hour
    return render(request, 'properties/list.html', {'properties': properties})

