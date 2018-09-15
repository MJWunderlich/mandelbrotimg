from django.core.validators import slug_unicode_re
from django.http import HttpResponse, HttpResponseBadRequest
from django.template import loader
from imagegen.models import GeneratedImage


def index(request, slug=None):
    template = loader.get_template('imageui/index.html')
    context = {'images': GeneratedImage.objects.all(), 'image_to_show': ''}
    if slug is not None:
        image_to_show = GeneratedImage.objects.filter(slug__endswith=slug)
        if image_to_show:
            context['image_to_show'] = image_to_show[0]
    return HttpResponse(template.render(context, request))

